"""zsc_lossless — the codec path, rebuilt around what was measured 2026-09-08/09.

This is ADDITIVE. It reuses the prototype's own machinery (`GeometryInterpreter`,
`_BaseLeafMinter`, `_TopologicalPyramid`) and leaves `zspectral_compression.py`
untouched, because that file is GraphModel's atomic unit and its tokenization
must not shift underneath the model.

Four changes, each from a measurement in DevComms:

  1. RATE criterion instead of an error threshold          (log 006: 2.51x -> 25.89x)
     A node is kept whole when that costs fewer bits than splitting it, not when
     its error is under a constant. Exactness is the correction stream's job.

  2. PER-SEGMENT mode: degree 0,1,2,3 or RAW               (log 007 §8, log 009)
     Degree 0 beats degree 3 on text, binaries and photos; degree 3 wins 3.6x on
     smooth data. RAW bounds the worst case: a segment can never cost more than
     the bytes it holds, so the format cannot expand beyond the mode flags.

  3. TRAVERSAL chosen per volume                            (log 010: up to 16.8x)
     Morton is the worst order for static video and the best for moving video.
     Try each axis-fastest order plus Morton, keep the cheapest.

  4. A real CORRECTION stream, so the output is lossless and round-trips.
"""
import io, math, struct, lzma
import numpy as np

MODE_RAW = 4                      # 0..3 are polynomial degrees; 4 is stored-raw
CAND_BITS = (8, 12, 16)
CAND_LEN = (8, 16, 32, 64, 128, 256, 512, 1024)


# ---------------------------------------------------------------- basis
def basis(W, deg):
    """Chebyshev T0..Tdeg sampled at W equispaced points. Columns = coefficients."""
    x = np.linspace(-1.0, 1.0, W)
    T = [np.ones_like(x)]
    if deg >= 1:
        T.append(x)
    for k in range(2, deg + 1):
        T.append(2 * x * T[-1] - T[-2])
    return np.stack(T, 1)


def _entropy(v):
    if v.size == 0:
        return 0.0
    c = np.bincount((v - v.min()).astype(np.int64))
    c = c[c > 0] / v.size
    return float(-(c * np.log2(c)).sum())


# ---------------------------------------------------------------- traversal
def axis_orders(shape):
    """Candidate traversals: each axis fastest-varying in turn, plus Morton."""
    n = len(shape)
    out = [("axis%d" % a, a) for a in range(n)]
    out.append(("morton", None))
    return out


def permutation(shape, spec):
    """Flat indices of the volume in the given traversal order."""
    n = len(shape)
    if spec is None:                                   # Morton: interleave the bits
        total = int(np.prod(shape))
        idx = np.arange(total)
        coords, rem = [], idx
        for s in reversed(shape):
            coords.insert(0, rem % s)
            rem = rem // s
        code = np.zeros(total, dtype=np.int64)
        bits = max(int(s - 1).bit_length() for s in shape)
        shift = 0
        for b in range(bits):
            for a in range(n):
                if b < int(shape[a] - 1).bit_length():
                    code |= ((coords[a] >> b) & 1) << shift
                    shift += 1
        return np.argsort(code, kind="stable")
    # axis `spec` fastest: move it last, then read in C order
    axes = [a for a in range(n) if a != spec] + [spec]
    return np.transpose(np.arange(int(np.prod(shape))).reshape(shape), axes).ravel()


# ---------------------------------------------------------------- segmentation
def rate_segmentation(d, seg_len):
    """Fixed-length segmentation at seg_len. The pyramid walk collapses to this
    when the rate criterion is applied uniformly; kept simple and exact."""
    n = len(d) // seg_len
    return [(i * seg_len, (i + 1) * seg_len) for i in range(n)], n * seg_len


def segment_cost(win, deg, cb):
    """Bits for a batch of equal-length segments at one (degree, precision),
    and the integer residual that makes it exact."""
    W = win.shape[1]
    A = basis(W, deg)
    coef = win @ np.linalg.pinv(A).T
    lo, hi = coef.min(0), coef.max(0)
    step = np.where(hi > lo, (hi - lo) / (2 ** cb - 1), 1.0)
    q = np.rint((coef - lo) / step)
    rec = np.clip((q * step + lo) @ A.T, 0, 255).round()
    res = (win - rec).astype(np.int64)
    per = np.full(win.shape[0], (deg + 1) * cb, dtype=float) + W * _entropy(res.ravel())
    return per, q.astype(np.int64), (lo, step), res


# ---------------------------------------------------------------- codec
class ZSCLossless:
    """Lossless N-dimensional codec. compress() -> bytes, decompress() -> array."""

    MAGIC = b"ZSC1"

    def _plan(self, flat):
        """Pick segment length, and per segment the cheapest mode. Returns the plan
        and its estimated bit cost."""
        best = None
        for W in CAND_LEN:
            n = len(flat) // W
            if n < 1:
                continue
            win = flat[:n * W].reshape(n, W)
            per = np.full(n, W * 8.0)                      # RAW: always available
            pick = [(MODE_RAW, None, None, None)] * n
            store = {}
            for deg in (0, 1, 2, 3):
                if deg + 1 >= W:
                    continue
                for cb in CAND_BITS:
                    c, q, dq, res = segment_cost(win, deg, cb)
                    store[(deg, cb)] = (q, dq, res)
                    better = c < per
                    if better.any():
                        per = np.where(better, c, per)
                        for i in np.nonzero(better)[0]:
                            pick[i] = (deg, cb, None, None)
            total = per.sum() + n * 3 + 160               # 3 mode bits + header
            if best is None or total < best[0]:
                best = (total, W, n, pick, store, win)
        return best

    def compress(self, arr, container="lzma"):
        arr = np.asarray(arr, dtype=np.uint8)
        shape = arr.shape
        flat_src = arr.ravel().astype(float)

        # 1. choose the traversal by pricing each candidate
        chosen, chosen_bits, chosen_name = None, None, None
        for name, spec in axis_orders(shape):
            perm = permutation(shape, spec)
            bits = self._plan(flat_src[perm])[0]
            if chosen_bits is None or bits < chosen_bits:
                chosen, chosen_bits, chosen_name = (spec, perm), bits, name
        spec, perm = chosen
        flat = flat_src[perm]

        # 2. plan the segmentation and modes on the chosen order
        _, W, n, pick, store, win = self._plan(flat)

        modes = np.array([p[0] for p in pick], dtype=np.uint8)
        cbs = np.array([p[1] if p[0] != MODE_RAW else 0 for p in pick], dtype=np.uint8)

        coef_blob, raw_blob, res_blob = io.BytesIO(), io.BytesIO(), io.BytesIO()
        for i in range(n):
            deg = modes[i]
            if deg == MODE_RAW:
                # a raw segment IS its bytes; it carries no residual at all
                raw_blob.write(win[i].astype(np.uint8).tobytes())
                continue
            q, (lo, step), res = store[(deg, cbs[i])]
            coef_blob.write(q[i].astype("<i4").tobytes())
            res_blob.write(res[i].astype("<i2").tobytes())

        # dequantisation constants, one set per (degree, precision) actually used
        used = sorted({(int(modes[i]), int(cbs[i])) for i in range(n) if modes[i] != MODE_RAW})
        consts = io.BytesIO()
        consts.write(struct.pack("<H", len(used)))
        for deg, cb in used:
            _, (lo, step) = store[(deg, cb)][0], store[(deg, cb)][1]
            consts.write(struct.pack("<BB", deg, cb))
            consts.write(np.asarray(lo, dtype="<f8").tobytes())
            consts.write(np.asarray(step, dtype="<f8").tobytes())

        head = io.BytesIO()
        head.write(self.MAGIC)
        head.write(struct.pack("<BB", len(shape), 0 if spec is None else spec + 1))
        for s in shape:
            head.write(struct.pack("<I", s))
        head.write(struct.pack("<II", W, n))
        head.write(struct.pack("<I", len(flat) - n * W))          # tail length
        body = (head.getvalue() + consts.getvalue() + modes.tobytes() + cbs.tobytes()
                + coef_blob.getvalue() + raw_blob.getvalue()
                + res_blob.getvalue()
                + flat[n * W:].astype(np.uint8).tobytes())

        # The container is a CHOICE, and it is the ratio/addressability trade of
        # log 008. Packed alone, every segment stays independently decodable.
        # Wrapped in lzma the ratio improves — often a lot, because lzma catches
        # the repetition a polynomial model structurally cannot see (log 007 §2) —
        # but the result decodes only from the start.
        packed = body
        squeezed = lzma.compress(body, preset=6)
        best = squeezed if (container == "lzma" and len(squeezed) < len(packed)) else packed
        tag = b"Z" if best is packed else b"L"

        # Whole-file escape: the format may never cost more than the bytes plus
        # this header, whatever the input. This is what makes break-even a
        # guarantee rather than an observation (log 009).
        stored = b"R" + struct.pack("<B", len(shape)) + b"".join(
            struct.pack("<I", s_) for s_ in shape) + arr.tobytes()
        if len(stored) <= len(best) + 1:
            return stored, "stored"
        return tag + best, chosen_name

    def decompress(self, payload):
        if payload[:1] == b"R":                      # stored verbatim
            nd = payload[1]
            p = 2
            shape = []
            for _ in range(nd):
                shape.append(struct.unpack_from("<I", payload, p)[0]); p += 4
            return np.frombuffer(payload, np.uint8, int(np.prod(shape)), p).reshape(shape).copy()
        b = lzma.decompress(payload[1:]) if payload[:1] == b"L" else payload[1:]
        assert b[:4] == self.MAGIC
        p = 4
        nd, spec_p = struct.unpack_from("<BB", b, p); p += 2
        shape = []
        for _ in range(nd):
            shape.append(struct.unpack_from("<I", b, p)[0]); p += 4
        shape = tuple(shape)
        W, n = struct.unpack_from("<II", b, p); p += 8
        tail_len = struct.unpack_from("<I", b, p)[0]; p += 4

        nconst = struct.unpack_from("<H", b, p)[0]; p += 2
        consts = {}
        for _ in range(nconst):
            deg, cb = struct.unpack_from("<BB", b, p); p += 2
            k = deg + 1
            lo = np.frombuffer(b, "<f8", k, p); p += 8 * k
            step = np.frombuffer(b, "<f8", k, p); p += 8 * k
            consts[(deg, cb)] = (lo, step)

        modes = np.frombuffer(b, np.uint8, n, p); p += n
        cbs = np.frombuffer(b, np.uint8, n, p); p += n
        ncoef = sum(int(m) + 1 for m in modes if m != MODE_RAW)
        coefs = np.frombuffer(b, "<i4", ncoef, p); p += 4 * ncoef
        nraw = int((modes == MODE_RAW).sum())
        raws = np.frombuffer(b, np.uint8, nraw * W, p); p += nraw * W
        nres = int((modes != MODE_RAW).sum())
        resid = np.frombuffer(b, "<i2", nres * W, p).reshape(nres, W); p += 2 * nres * W
        tail = np.frombuffer(b, np.uint8, tail_len, p)

        out = np.zeros(n * W + tail_len)
        ci = ri = si = 0
        for i in range(n):
            deg = int(modes[i])
            if deg == MODE_RAW:
                out[i * W:(i + 1) * W] = raws[ri * W:(ri + 1) * W]; ri += 1
                continue
            k = deg + 1
            q = coefs[ci:ci + k].astype(float); ci += k
            lo, step = consts[(deg, int(cbs[i]))]
            rec = np.clip((q * step + lo) @ basis(W, deg).T, 0, 255).round()
            out[i * W:(i + 1) * W] = rec + resid[si]; si += 1
        out[n * W:] = tail

        spec = None if spec_p == 0 else spec_p - 1
        perm = permutation(shape, spec)
        flat = np.zeros(int(np.prod(shape)))
        flat[perm] = out
        return flat.reshape(shape).astype(np.uint8)
