import numpy as np, math, lzma
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
    for W in (8,16,32,64,128,256):
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
def morton3(n):
    o=np.empty(n**3,dtype=np.int64)
    for i in range(n**3):
        x=y=z=0
        for b in range(11):
            x|=((i>>(3*b))&1)<<b; y|=((i>>(3*b+1))&1)<<b; z|=((i>>(3*b+2))&1)<<b
        o[i]=(x*n+y)*n+z
    return o

X=Y=T=32
xx,yy=np.meshgrid(np.arange(X),np.arange(Y),indexing="ij")
tex=np.clip(128+90*np.sin(xx/5.0)*np.cos(yy/7.0),0,255)
photo=np.frombuffer(open("/tmp/xc/photo_00.bin","rb").read(),dtype=np.uint8).reshape(128,256)

vids={}
vids["static scene, no change"]=np.repeat(tex[:,:,None],T,axis=2)
vids["static scene, slow fade"]=np.clip(tex[:,:,None]*(0.6+0.4*np.sin(np.arange(T)/6.0))[None,None,:],0,255)
v=np.zeros((X,Y,T))
for k in range(T):
    cx,cy=8+k*0.4,16+6*math.sin(k/5.0)
    v[:,:,k]=np.where((xx-cx)**2+(yy-cy)**2<36,220,40)
vids["moving disc"]=v
vids["real photo, panning"]=np.stack([photo[10:10+X,k:k+Y] for k in range(T)],axis=2).astype(float)

M3=morton3(32)
print("VIDEO: the SAME volume, only the traversal order changes  (32x32x32, lossless)\n")
print("%-26s %9s %9s %9s %9s"%("content","per-frame","frame-major","TIME-major","morton 3-D"))
print("%-26s %9s %9s %9s %9s"%("","(2-D only)","x fastest","t fastest","interleaved"))
print("-"*70)
for nm,vol in vids.items():
    vol=np.clip(vol,0,255); N=8*vol.size
    perframe=sum(price(vol[:,:,k].ravel()) for k in range(T))
    framemajor=price(np.transpose(vol,(2,0,1)).ravel())   # t,y,x  -> x fastest
    timemajor =price(vol.ravel())                          # x,y,t  -> t fastest
    mort      =price(vol.ravel()[M3])
    print("%-26s %8.2fx %8.2fx %8.2fx %8.2fx"%(nm,N/perframe,N/framemajor,N/timemajor,N/mort))
