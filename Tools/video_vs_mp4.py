#!/usr/bin/env python3
"""video_vs_mp4 -- one real video clip, compressed by ZSC and by the codecs mp4 files use.

Every method compresses the SAME frames: the brightness channel (luma) of the
clip, shrunk and cropped to a small block so this stays a quick verification
run. Every size is a real byte count. "exact" means every pixel came back.

The volume ZSC sees is laid out (vertical, horizontal, time), so ZSC's
reading order is reported by those names, never by axis number.

usage:
    python3 Tools/video_vs_mp4.py VIDEO WORKDIR [--frames 64] [--shrink 5] [--rows 128]
"""
import argparse, json, lzma, math, subprocess, sys, time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from zsc_lossless import ZSCLossless  # noqa: E402

AXIS_NAMES = {0: "vertical", 1: "horizontal", 2: "time"}


def reading_order_name(code):
    """The codec reports 'axisN', 'morton' or 'stored'; say it in words."""
    if code.startswith("axis"):
        return AXIS_NAMES[int(code[4:])] + "-first"
    return {"morton": "Morton (small blocks of space and time)",
            "stored": "stored raw (no curve helped)"}.get(code, code)


# ---------------------------------------------------------------- the frames
def load_luma(video, frames, shrink, rows):
    """Decode, keep the luma plane byte-for-byte, shrink by block averaging,
    crop `rows` rows from the middle. Returns (time, vertical, horizontal)."""
    import av
    out, fps = [], None
    with av.open(str(video)) as c:
        fps = c.streams.video[0].average_rate
        for f in c.decode(video=0):
            yuv = f.to_ndarray(format="yuv420p")
            y = yuv[: f.height].astype(np.float64)
            H = (y.shape[0] // shrink) * shrink
            W = (y.shape[1] // shrink) * shrink
            y = y[:H, :W].reshape(H // shrink, shrink, W // shrink, shrink).mean(axis=(1, 3))
            top = (y.shape[0] - rows) // 2
            out.append(np.rint(y[top: top + rows]).astype(np.uint8))
            if len(out) == frames:
                break
    return np.stack(out), fps


def psnr(a, b):
    """Peak signal-to-noise ratio in decibels; infinite when identical."""
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10.0 * math.log10(255.0 ** 2 / mse)


# ---------------------------------------------------------------- ffmpeg
def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def ff_encode(raw_path, shape, fps, out_path, codec_args):
    T, V, H = shape
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{H}x{V}", "-r", str(fps),
           "-i", str(raw_path)] + codec_args + [str(out_path)]
    subprocess.run(cmd, check=True)


def ff_decode(path, shape):
    T, V, H = shape
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-i", str(path),
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    b = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(b, np.uint8)[: T * V * H].reshape(T, V, H)


# ---------------------------------------------------------------- ZSC lossy
def load_prototype():
    """The prototype's classes, without running the demonstration cells at the
    bottom of the file."""
    src = (REPO / "zspectral_compression.py").read_text()
    g = {}
    cut = src.index("def test_ultimate_quadtree_compression")
    exec(compile(src[:cut], "zspectral_compression", "exec"), g)
    return g


def zsc_lossy(g, vol_vht, threshold, k=256):
    """The prototype's own lossy path. Returns its own byte count, the payload
    written out as real bytes and squeezed by xz, the segment count, and the
    reconstruction in (vertical, horizontal, time)."""
    import torch
    cfg = g["VisionGeometryConfig"]()
    cfg.merge_threshold = threshold
    comp = g["ZSpectralCompressor"](g["Interface"](cfg), k_clusters=k)
    t = torch.from_numpy(vol_vht.astype(np.float32) / 255.0)
    meta = {"shape": tuple(t.shape)}
    with torch.no_grad():
        pay = comp.compress(t, meta)
        rec = comp.decompress(pay, meta)
    counted = int(comp.calculate_metrics(t, pay)["compressed_bytes"])
    blob = (pay["labels"].cpu().numpy().astype(np.uint8 if k <= 256 else np.uint16).tobytes()
            + pay["c0_quantized"].cpu().numpy().astype(np.uint8).tobytes()
            + pay["codebook"].cpu().numpy().astype(np.float32).tobytes()
            + pay["topology_bytes"].cpu().numpy().astype(np.uint8).tobytes())
    real = len(lzma.compress(blob, preset=9)) + 16          # + a small header
    recb = np.clip(rec.cpu().numpy() * 255.0, 0, 255).round().astype(np.uint8)
    return counted, real, int(len(pay["labels"])), recb


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("workdir")
    ap.add_argument("--frames", type=int, default=64)
    ap.add_argument("--shrink", type=int, default=5)
    ap.add_argument("--rows", type=int, default=128)
    ap.add_argument("--zsc-thresholds", default="0.002,0.005,0.01,0.02")
    ap.add_argument("--crfs", default="18,23,28,33")
    a = ap.parse_args()

    work = Path(a.workdir)
    work.mkdir(parents=True, exist_ok=True)
    vol, fps = load_luma(a.video, a.frames, a.shrink, a.rows)       # (time, vertical, horizontal)
    shape = vol.shape
    raw = vol.tobytes()                                              # frame after frame, row after row
    (work / "raw.gray").write_bytes(raw)
    vht = np.ascontiguousarray(np.transpose(vol, (1, 2, 0)))         # (vertical, horizontal, time)
    rows = []

    def add(group, method, nbytes, rec=None, exact=None, secs=None, note=""):
        if rec is not None:
            q = psnr(vol, rec)
            exact = bool(np.array_equal(vol, rec))
        else:
            q = float("inf") if exact else None
        rows.append(dict(group=group, method=method, bytes=int(nbytes),
                         ratio=len(raw) / nbytes, exact=exact, psnr=q,
                         seconds=secs, note=note))
        print("  %-9s %-44s %9d B %8.2fx  %-5s %s  %s" % (
            group, method, nbytes, len(raw) / nbytes, exact,
            "inf" if q == float("inf") else ("%.2f dB" % q if q is not None else "-"),
            note), flush=True)

    print("frames: %d x %d vertical x %d horizontal, luma only, %d raw bytes" % (
        shape[0], shape[1], shape[2], len(raw)))

    # ---- lossless: every pixel must come back
    add("lossless", "raw frames, no compression", len(raw), exact=True)
    t0 = time.time(); xz = lzma.compress(raw, preset=9)
    add("lossless", "xz -9 on the raw frames", len(xz), exact=lzma.decompress(xz) == raw,
        secs=time.time() - t0)
    for name, args, fn in (
            ("FFV1, .mkv (a lossless video codec)", ["-c:v", "ffv1", "-level", "3"], "ffv1.mkv"),
            ("H.264 lossless, .mp4", ["-c:v", "libx264", "-preset", "medium", "-qp", "0"],
             "h264_lossless.mp4")):
        t0 = time.time(); ff_encode(work / "raw.gray", shape, fps, work / fn, args)
        add("lossless", name, (work / fn).stat().st_size, rec=ff_decode(work / fn, shape),
            secs=time.time() - t0)

    zc = ZSCLossless()
    for label, cont in (("ZSC lossless, addressable", "none"),
                        ("ZSC lossless, sequential", "lzma")):
        t0 = time.time(); pay, order = zc.compress(vht, container=cont)
        secs = time.time() - t0
        back = zc.decompress(pay)
        add("lossless", label, len(pay), exact=bool(np.array_equal(back, vht)), secs=secs,
            note="reading order: " + reading_order_name(order))

    # ---- lossy: what a normal mp4 is
    for crf in [int(c) for c in a.crfs.split(",")]:
        fn = "h264_crf%d.mp4" % crf
        t0 = time.time()
        ff_encode(work / "raw.gray", shape, fps, work / fn,
                  ["-c:v", "libx264", "-preset", "medium", "-crf", str(crf)])
        add("lossy", "H.264 crf %d, .mp4%s" % (crf, "  (x264's default)" if crf == 23 else ""),
            (work / fn).stat().st_size, rec=ff_decode(work / fn, shape), secs=time.time() - t0)

    g = load_prototype()
    for thr in [float(x) for x in a.zsc_thresholds.split(",")]:
        t0 = time.time()
        counted, real, ntok, recb = zsc_lossy(g, vht, thr)
        add("lossy", "ZSC lossy (prototype), threshold %g" % thr, real,
            rec=np.ascontiguousarray(np.transpose(recb, (2, 0, 1))), secs=time.time() - t0,
            note="%d segments; prototype's own count %d B" % (ntok, counted))

    (work / "results.json").write_text(json.dumps(dict(
        shape_time_vertical_horizontal=list(shape), raw_bytes=len(raw), rows=rows),
        indent=1, default=str))
    print("wrote", work / "results.json")


if __name__ == "__main__":
    main()
