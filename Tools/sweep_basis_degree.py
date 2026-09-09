import numpy as np, math, lzma
from collections import Counter
def H0(v):
    c=Counter(np.asarray(v).tolist()); n=len(v)
    return -sum((k/n)*math.log2(k/n) for k in c.values()) if n else 0.0
def basis(W,deg):
    x=np.linspace(-1,1,W)
    T=[np.ones_like(x),x,2*x**2-1,4*x**3-3*x,8*x**4-8*x**2+1]
    return np.stack(T[:deg+1],1)
def bits(d,W,deg,cb):
    A=basis(W,deg); P=np.linalg.pinv(A); n=len(d)//W
    win=d[:n*W].reshape(n,W); coef=win@P.T
    lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**cb-1),1.0)
    q=np.rint((coef-lo)/step)*step+lo
    rec=np.clip(q@A.T,0,255).round().astype(np.int64)
    res=(win.astype(np.int64)-rec).ravel()
    return n*(deg+1)*cb + len(res)*H0(res) + 256, len(res)*H0(res), n*(deg+1)*cb

print("LOSSLESS ratio by basis degree — coefficients per segment = degree+1")
print("(every configuration restores 100% of bytes; segment length and coefficient")
print(" precision are swept and the best kept for each degree)\n")
print("%-16s %8s %8s %8s %8s %10s" % ("file","deg 0","deg 1","deg 2","deg 3","xz -9"))
for name,path in [("python_source","/samples/python_source.bin"),
                  ("english_prose","/samples/english_prose.bin"),
                  ("elf_binary","/samples/elf_binary.bin"),
                  ("photo tile","/tmp/xc/photo_00.bin"),
                  ("smooth_1d","/samples/smooth_1d.bin")]:
    raw=np.frombuffer(open(path,"rb").read()[:32768],dtype=np.uint8); d=raw.astype(float)
    xz=8*raw.size/(8*len(lzma.compress(raw.tobytes(),preset=9)))
    row=[]
    for deg in (0,1,2,3):
        best=min(bits(d,W,deg,cb)[0] for W in (2,4,8,16,32,64,128,256,512,1024)
                                      for cb in (8,12,16,20) if W>deg)
        row.append(8*raw.size/best)
    print("%-16s %7.2fx %7.2fx %7.2fx %7.2fx %9.2fx" % (name,row[0],row[1],row[2],row[3],xz))

print("\nwhere the bits go, at the settings drawn in the figure (160 bytes = 1280 bits):")
for nm,segs,deg in (("text  @0.05", 31, 3), ("smooth @0.05", 3, 3)):
    print("   %-14s %2d segments x %d coefficients x 12 bits = %5d bits of coefficients  (%.0f%% of the raw file)"
          % (nm, segs, deg+1, segs*(deg+1)*12, 100.0*segs*(deg+1)*12/1280))
