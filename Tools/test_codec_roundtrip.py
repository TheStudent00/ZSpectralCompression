import numpy as np, math, lzma, sys
sys.path.insert(0,"/tmp/src")
from zsc_lossless import ZSCLossless
c=ZSCLossless()
def run(name, arr):
    raw=arr.astype(np.uint8).tobytes()
    pl,order=c.compress(arr,container="lzma")
    pa,_    =c.compress(arr,container="none")
    ok = np.array_equal(c.decompress(pl),arr.astype(np.uint8)) and np.array_equal(c.decompress(pa),arr.astype(np.uint8))
    xz=len(raw)/len(lzma.compress(raw,preset=9))
    print("%-30s %8.2fx %10.2fx %7.2fx  %-8s %s"
          % (name, len(raw)/len(pa), len(raw)/len(pl), xz, order, "EXACT" if ok else "*** MISMATCH ***"))
    return ok

allok=True
print("%-30s %8s %10s %7s  %-8s %s"%("input","addressable","sequential","xz -9","order","round-trip"))
print("-"*82)
for nm,p in [("python source","/samples/python_source.bin"),
             ("english prose","/samples/english_prose.bin"),
             ("elf binary","/samples/elf_binary.bin"),
             ("pure random","/dev/urandom")]:
    d=np.frombuffer(open(p,"rb").read(32768),dtype=np.uint8)
    allok &= run(nm, d)
allok &= run("photo tile 2-D", np.frombuffer(open("/tmp/xc/photo_00.bin","rb").read(),dtype=np.uint8).reshape(128,256))
allok &= run("smooth signal 1-D", np.frombuffer(open("/samples/smooth_1d.bin","rb").read()[:32768],dtype=np.uint8))

X=Y=T=32
xx,yy=np.meshgrid(np.arange(X),np.arange(Y),indexing="ij")
tex=np.clip(128+90*np.sin(xx/5.0)*np.cos(yy/7.0),0,255)
allok &= run("video: static scene 3-D", np.repeat(tex[:,:,None],T,axis=2).astype(np.uint8))
v=np.zeros((X,Y,T))
for k in range(T):
    cx,cy=8+k*0.4,16+6*math.sin(k/5.0)
    v[:,:,k]=np.where((xx-cx)**2+(yy-cy)**2<36,220,40)
allok &= run("video: moving disc 3-D", v.astype(np.uint8))
S=16
g=np.stack(np.meshgrid(*[np.arange(S)]*3,indexing="ij"),0).astype(float)
f=np.clip(128+90*np.sin(g[0]/3.0)*np.cos(g[1]/4.0)*np.sin(g[2]/5.0),0,255)
allok &= run("game: static 3-D field x time", np.repeat(f[...,None],16,axis=3).astype(np.uint8))
rng=np.random.default_rng(3)
terr=(rng.integers(0,4,(S,S,S))*70).astype(np.uint8)
allok &= run("game: voxel terrain x time", np.repeat(terr[...,None],16,axis=3))
print("\nALL ROUND-TRIPS EXACT" if allok else "\nSOME ROUND-TRIPS FAILED")
