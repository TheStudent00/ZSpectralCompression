import numpy as np, math, os, lzma, zstandard as zstd
from collections import Counter
def H0(v):
    v=np.asarray(v); c=Counter(v.tolist()); n=len(v)
    return -sum((k/n)*math.log2(k/n) for k in c.values()) if n else 0.0
def cheb(W,K):
    x=np.linspace(-1,1,W); T=[np.ones_like(x)]
    if K>1: T.append(x)
    for k in range(2,K): T.append(2*x*T[-1]-T[-2])
    return np.stack(T[:K],1)

def zsc(d, W, escape):
    """per-segment: pick the cheapest of degree 0..3, or RAW if escape is on.
       1 flag byte per segment covers the mode."""
    n=len(d)//W
    if n==0: return 1e18
    win=d[:n*W].reshape(n,W)
    per_seg=np.full(n, W*8.0 if escape else 1e18)      # raw cost per segment
    for K in (1,2,3,4):
        if K>=W: continue
        A=cheb(W,K); P=np.linalg.pinv(A); coef=win@P.T
        for cb in (8,12,16):
            lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**cb-1),1.0)
            q=np.rint((coef-lo)/step)*step+lo
            rec=np.clip(q@A.T,0,255).round()
            res=(win-rec).astype(np.int64)
            h=H0(res.ravel())                          # shared residual alphabet
            c=K*cb + W*h
            per_seg=np.minimum(per_seg, c)
    return per_seg.sum() + n*2 + 256                   # 2 bits of mode flag per segment

zc=zstd.ZstdCompressor(level=19,write_checksum=False,write_content_size=False)
EMPTY=len(zc.compress(b""))
rng=np.random.default_rng(0)

cases=[]
cases.append(("pure random bytes", bytes(rng.integers(0,256,32768,dtype=np.uint8))))
cases.append(("already zstd-compressed", zc.compress(open("/samples/python_source.bin","rb").read()[:65536])[:32768]))
cases.append(("PNG file bytes", open("/samples/png_image.bin","rb").read()[:32768]))
cases.append(("JPEG file bytes", open("/samples/jpeg_image.bin","rb").read()[:32768]))
cases.append(("alternating 0,255", bytes(np.tile([0,255],16384).astype(np.uint8))))
cases.append(("sawtooth period 7", bytes((np.arange(32768)%7*36).astype(np.uint8))))
cases.append(("ELF binary", open("/samples/elf_binary.bin","rb").read()[:32768]))
cases.append(("python source", open("/samples/python_source.bin","rb").read()[:32768]))
cases.append(("photo tile", open("/tmp/xc/photo_00.bin","rb").read()[:32768]))
cases.append(("smooth signal", open("/samples/smooth_1d.bin","rb").read()[:32768]))

print("WORST-CASE TEST — is ZSC ever below 1.00x?   (256-byte random-access granularity)\n")
print("%-26s %12s %14s %11s" % ("input","ZSC as-is","ZSC + escape","zstd @256B"))
print("-"*68)
for nm,b in cases:
    d=np.frombuffer(b,dtype=np.uint8).astype(float); n=len(b)
    a=8*n/zsc(d,256,False); e=8*n/zsc(d,256,True)
    tot=sum(len(zc.compress(b[i:i+256])) for i in range(0,n,256)) - ((n+255)//256)*EMPTY
    print("%-26s %11.3fx %13.3fx %10.3fx %s" % (nm,a,e,n/max(1,tot),"" if a>=1.0 else "  <-- BELOW 1.0"))
