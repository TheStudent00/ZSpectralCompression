import numpy as np, math, hashlib, lzma
from collections import Counter
def H0(v):
    v=np.asarray(v); c=Counter(v.tolist()); n=len(v)
    return -sum((k/n)*math.log2(k/n) for k in c.values()) if n else 0.0
def cheb(W,K):
    x=np.linspace(-1,1,W); T=[np.ones_like(x)]
    if K>1: T.append(x)
    for k in range(2,K): T.append(2*x*T[-1]-T[-2])
    return np.stack(T[:K],1)
def price(d):
    best=1e18
    for W in (8,16,32,64,128,256,512):
        n=len(d)//W
        if n<1: continue
        win=d[:n*W].reshape(n,W); per=np.full(n,W*8.0)
        for K in (1,2,3,4):
            if K>=W: continue
            A=cheb(W,K); P=np.linalg.pinv(A); coef=win@P.T
            for cb in (8,12,16):
                lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**cb-1),1.0)
                q=np.rint((coef-lo)/step)*step+lo
                res=(win-np.clip(q@A.T,0,255).round()).astype(np.int64)
                per=np.minimum(per,K*cb+W*H0(res.ravel()))
        best=min(best,per.sum()+n*2+256)
    return best
def morton_idx(n):
    o=[]
    for i in range(n*n):
        x=y=0
        for b in range(16):
            x|=((i>>(2*b))&1)<<b; y|=((i>>(2*b+1))&1)<<b
        o.append(y*n+x)
    return np.array(o)
def hilbert_idx(n):
    o=[]
    for d in range(n*n):
        x=y=0; t=d; s=1
        while s<n:
            rx=1&(t//2); ry=1&(t^rx)
            if ry==0:
                if rx==1: x=s-1-x; y=s-1-y
                x,y=y,x
            x+=s*rx; y+=s*ry; t//=4; s*=2
        o.append(y*n+x)
    return np.array(o)

N=128
photo=np.frombuffer(open("/tmp/xc/photo_00.bin","rb").read(),dtype=np.uint8).reshape(128,256)[:,:128].astype(float)
xx,yy=np.meshgrid(np.arange(N),np.arange(N),indexing="ij")
smooth=np.clip(128+90*np.sin(xx/19.0)*np.cos(yy/23.0),0,255)
noise=np.random.default_rng(1).integers(0,256,(N,N)).astype(float)

MI,HI=morton_idx(N),hilbert_idx(N)
print("SAME DATA, SAME FIT — only the traversal order changes  (%dx%d, lossless)\n"%(N,N))
print("%-16s %10s %10s %10s   %s"%("image","raster","morton","hilbert","hilbert vs morton"))
print("-"*72)
for nm,img in (("photo tile",photo),("smooth 2-D field",smooth),("random noise",noise)):
    f=img.ravel(); n8=8*f.size
    r=n8/price(f); m=n8/price(f[MI]); h=n8/price(f[HI])
    print("%-16s %9.2fx %9.2fx %9.2fx   %+.0f%%"%(nm,r,m,h,100*(h/m-1)))

print("\nand the edit-locality property, re-measured on both curves")
print("(1024x1024, 4096-byte chunks, count how many chunk hashes change)")
def chunks(order,img,CH=4096):
    flat=img.ravel()[order]; out=[]
    for i in range(0,len(flat),CH):
        out.append(hashlib.blake2b(flat[i:i+CH].astype(np.uint8).tobytes(),digest_size=8).digest())
    return out
M=1024
MI2,HI2=morton_idx(M),hilbert_idx(M)
base=((np.arange(M)[:,None]**2+np.arange(M)[None,:]**2)%251).astype(np.uint8)
print("%-26s %10s %10s"%("edit","morton","hilbert"))
for lbl,(x0,y0,w,h) in (("64x64 square",(256,256,64,64)),("128x128 square",(256,256,128,128)),
                        ("one full row",(0,512,M,1)),("one full column",(512,0,1,M))):
    e=base.copy(); e[y0:y0+h,x0:x0+w]=7
    cm=sum(1 for a,b in zip(chunks(MI2,base),chunks(MI2,e)) if a!=b)
    ch=sum(1 for a,b in zip(chunks(HI2,base),chunks(HI2,e)) if a!=b)
    print("%-26s %8d/256 %8d/256"%(lbl,cm,ch))
