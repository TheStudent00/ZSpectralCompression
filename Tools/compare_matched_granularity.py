import numpy as np, math, lzma, zstandard as zstd
from collections import Counter
zc=zstd.ZstdCompressor(level=19,write_checksum=False,write_content_size=False)
EMPTY=len(zc.compress(b""))
def H0(v):
    v=np.asarray(v); c=Counter(v.tolist()); n=len(v)
    return -sum((k/n)*math.log2(k/n) for k in c.values()) if n else 0.0
def cheb(W,K):
    x=np.linspace(-1,1,W); T=[np.ones_like(x)]
    if K>1: T.append(x)
    for k in range(2,K): T.append(2*x*T[-1]-T[-2])
    return np.stack(T[:K],1)
def zsc_bits(d,W):
    best=1e18
    for K in (1,2,3,4):
        if K>=W: continue
        A=cheb(W,K); P=np.linalg.pinv(A); n=len(d)//W
        win=d[:n*W].reshape(n,W); coef=win@P.T
        for cb in (8,12,16):
            lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**cb-1),1.0)
            q=np.rint((coef-lo)/step)*step+lo
            rec=np.clip(q@A.T,0,255).round().astype(np.int64)
            res=(win.astype(np.int64)-rec).ravel()
            best=min(best, n*K*cb + len(res)*H0(res))
    return best

print("SAME RANDOM-ACCESS GRANULARITY, BOTH LOSSLESS")
print("(both can decode one block/segment without touching the rest)\n")
for nm,p in [("python_source","/samples/python_source.bin"),
             ("elf_binary","/samples/elf_binary.bin"),
             ("photo tile","/tmp/xc/photo_00.bin"),
             ("smooth_1d","/samples/smooth_1d.bin")]:
    raw=open(p,"rb").read()[:32768]; n=len(raw)
    d=np.frombuffer(raw,dtype=np.uint8).astype(float)
    xz=8*n/(8*len(lzma.compress(raw,preset=9)))
    print("=== %s   (whole-file, sequential-only: xz -9 = %.2fx) ===" % (nm,xz))
    print("%12s %10s %10s" % ("granularity","ZSC","zstd -19"))
    for B in (16,32,64,128,256,512,1024):
        zb=zsc_bits(d,B)
        tot=sum(len(zc.compress(raw[i:i+B])) for i in range(0,n,B))
        tot-= ((n+B-1)//B)*EMPTY
        print("%11dB %9.2fx %9.2fx" % (B, 8*n/zb, n/max(1,tot)))
    print()
