import numpy as np, math, lzma
from collections import Counter
def H0(v):
    v=np.asarray(v); c=Counter(v.tolist()); n=len(v)
    return -sum((k/n)*math.log2(k/n) for k in c.values()) if n else 0.0

def cheb(W,K):
    x=np.linspace(-1,1,W)
    T=[np.ones_like(x)]
    if K>1: T.append(x)
    for k in range(2,K): T.append(2*x*T[-1]-T[-2])
    return np.stack(T[:K],1)
def dct(W,K):
    n=np.arange(W)[:,None]; k=np.arange(K)[None,:]
    return np.cos(np.pi*(n+0.5)*k/W)
def hadamard(W,K):
    H=np.ones((1,1))
    while H.shape[0]<W: H=np.block([[H,H],[H,-H]])
    changes=np.sum(np.abs(np.diff(np.sign(H),axis=1))>0,axis=1)   # sequency order
    H=H[np.argsort(changes)]
    return H[:K].T
def haar(W,K):
    H=np.ones((1,1))
    while H.shape[0]<W:
        n=H.shape[0]
        H=np.vstack([np.kron(H,[1,1]), np.kron(np.eye(n),[1,-1])])/math.sqrt(2)
    return H[:K].T
BASES={"chebyshev":cheb,"dct":dct,"walsh":hadamard,"haar":haar}

def cost(d,W,K,cb,mk,vmax=255):
    A=mk(W,K); P=np.linalg.pinv(A); n=len(d)//W
    if n==0: return 1e18
    win=d[:n*W].reshape(n,W); coef=win@P.T
    lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**cb-1),1.0)
    q=np.rint((coef-lo)/step)*step+lo
    rec=np.clip(q@A.T,0,vmax).round().astype(np.int64)
    res=(win.astype(np.int64)-rec).ravel()
    return n*K*cb + len(res)*H0(res) + 256
def best(d,mk,vmax=255,Ws=(4,8,16,32,64,128,256,512),Ks=(2,4,8),cbs=(8,12,16)):
    return min(cost(d,W,K,cb,mk,vmax) for W in Ws for K in Ks for cb in cbs if K<W)

FILES=[("python_source","/samples/python_source.bin"),
       ("english_prose","/samples/english_prose.bin"),
       ("elf_binary","/samples/elf_binary.bin"),
       ("photo tile","/tmp/xc/photo_00.bin"),
       ("smooth_1d","/samples/smooth_1d.bin")]

print("=== 1. DOES A DIFFERENT BASIS HELP?  (lossless ratio, each basis given its best W/K/precision) ===\n")
print("%-16s %10s %8s %8s %8s %9s" % ("file","chebyshev","dct","walsh","haar","xz -9"))
data={}
for nm,p in FILES:
    raw=np.frombuffer(open(p,"rb").read()[:32768],dtype=np.uint8); d=raw.astype(float); data[nm]=(raw,d)
    xz=8*raw.size/(8*len(lzma.compress(raw.tobytes(),preset=9)))
    r=[8*raw.size/best(d,BASES[b]) for b in ("chebyshev","dct","walsh","haar")]
    print("%-16s %9.2fx %7.2fx %7.2fx %7.2fx %8.2fx" % (nm,r[0],r[1],r[2],r[3],xz))

print("\n=== 2. SMALLER WORDS: split each byte into nibbles / 2-bit words ===")
print("(each sub-stream compressed separately with its best basis; bits summed)\n")
print("%-16s %10s %10s %10s %10s" % ("file","8-bit","two 4-bit","four 2-bit","eight 1-bit"))
for nm,_ in FILES:
    raw,d=data[nm]; N=raw.size*8
    b8 = min(best(d,BASES[b]) for b in BASES)
    def split(nbits):
        tot=0; m=(1<<nbits)-1
        for sh in range(0,8,nbits):
            s=((raw>>sh)&m).astype(float)
            tot+=min(best(s,BASES[b],vmax=m) for b in BASES)
        return tot
    print("%-16s %9.2fx %9.2fx %9.2fx %9.2fx"
          % (nm, N/b8, N/split(4), N/split(2), N/split(1)))

print("\n=== 3. RECURSION: run ZSC again on its own patch stream ===")
print("(does the leftover compress, or is it exactly the part the model cannot see?)\n")
print("%-16s %14s %16s %14s" % ("file","patch entropy","ZSC on patches","verdict"))
for nm,_ in FILES:
    raw,d=data[nm]
    # take the best single-pass configuration, then look at what it left behind
    bw,bk,bc,bb=None,None,None,1e18
    for W in (8,16,32,64,128,256):
        for K in (2,4,8):
            for cb in (8,12,16):
                if K>=W: continue
                c=cost(d,W,K,cb,BASES["chebyshev"])
                if c<bb: bb,bw,bk,bc=c,W,K,cb
    A=BASES["chebyshev"](bw,bk); P=np.linalg.pinv(A); n=len(d)//bw
    win=d[:n*bw].reshape(n,bw); coef=win@P.T
    lo,hi=coef.min(0),coef.max(0); step=np.where(hi>lo,(hi-lo)/(2**bc-1),1.0)
    q=np.rint((coef-lo)/step)*step+lo
    res=(win.astype(np.int64)-np.clip(q@A.T,0,255).round().astype(np.int64)).ravel()
    flat_bits=len(res)*H0(res)
    shifted=(res-res.min()).astype(float); vmax=float(shifted.max()) if shifted.max()>0 else 1.0
    zsc_bits=min(best(shifted,BASES[b],vmax=vmax) for b in BASES)
    print("%-16s %13.0f b %15.0f b %14s"
          % (nm, flat_bits, zsc_bits, "helps" if zsc_bits<flat_bits*0.98 else "no gain"))
