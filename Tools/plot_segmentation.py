import numpy as np, torch, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
src=open("/tmp/zsc.py").read(); g={}
exec(compile(src[:src.index("def test_ultimate_quadtree_compression")],"p","exec"),g)

def zsc(arr,thr):
    cfg=g["VisionGeometryConfig"](); cfg.merge_threshold=thr
    geo=g["GeometryInterpreter"](cfg); enc=g["LatentEncoding"](cfg)
    t=torch.from_numpy(arr.astype(np.float32)/255.0)
    flat,iv=geo.flatten_to_1d(t,{"shape":tuple(t.shape)})
    pyr=enc.pyramid.build(enc.minter.mint(flat,iv))
    ivs,sl=enc.walker.walk(pyr)
    return sl, enc.fitter.fit(flat,ivs,sl)[:,0,:].numpy(), flat.numpy()*255.0

def draw(axU,axL,arr,thr,title,note):
    sl,coef,orig=zsc(arr,thr); n=len(arr)
    axU.bar(np.arange(n),orig[:n],width=0.86,color="#c3cfe0",edgecolor="none",zorder=1)
    patch=np.zeros(n,dtype=int); segs=0
    for k,(s,e) in enumerate(sl):
        if s>=n: continue
        segs+=1; L=e-s
        xs=np.linspace(-1,1,L); A=np.stack([np.ones_like(xs),xs,2*xs**2-1,4*xs**3-3*xs],1)
        rec=np.clip((A@coef[k])*255.0,0,255).round()
        patch[s:min(e,n)]=(orig[s:min(e,n)].round()-rec[:min(e,n)-s]).astype(int)
        xd=np.linspace(-1,1,max(80,L*10)); Ad=np.stack([np.ones_like(xd),xd,2*xd**2-1,4*xd**3-3*xd],1)
        axU.plot(np.linspace(s,e-1,len(xd)),(Ad@coef[k])*255.0,color="#b3324a",lw=1.9,zorder=3)
        axU.axvline(s-0.5,color="#59708c",lw=0.8,ls=":",zorder=2)
    ex=100.0*np.mean(patch==0)
    axU.set_title("%s\n%d segments over %d bytes (mean %.1f)  |  %.1f%% need NO patch  |  %s"
                  %(title,segs,n,n/segs,ex,note),fontsize=10,loc="left")
    axU.set_xlim(-1,n); axU.set_ylim(0,265); axU.set_ylabel("byte value")
    axU.set_xticklabels([])
    axL.bar(np.arange(n),patch,width=0.86,
            color=np.where(patch==0,"#dfe5ee","#d98b3a"),edgecolor="none")
    axL.axhline(0,color="#59708c",lw=0.6)
    axL.set_xlim(-1,n); axL.set_ylabel("patch")
    m=max(4,int(np.abs(patch).max())); axL.set_ylim(-m*1.15,m*1.15)

N=160
txt=np.frombuffer(open("/samples/python_source.bin","rb").read()[2100:2100+N],dtype=np.uint8)
sig=np.array([max(0,min(255,round(128+118*math.sin(n/13.7)))) for n in range(N)],dtype=np.uint8)

fig=plt.figure(figsize=(15,13))
gs=GridSpec(6,1,height_ratios=[3,1,3,1,3,1],hspace=0.42)
P=[(fig.add_subplot(gs[i]),fig.add_subplot(gs[i+1])) for i in (0,2,4)]
draw(*P[0],txt,0.002,"PYTHON SOURCE, threshold 0.002",
     "every segment is the 4-byte minimum: 4 coefficients to describe 4 bytes")
draw(*P[1],txt,0.05,"PYTHON SOURCE, threshold 0.05",
     "the curve is now allowed to miss, and it misses almost everywhere")
draw(*P[2],sig,0.05,"SMOOTH SIGNAL, threshold 0.05  (identical setting to the panel above)",
     "one curve covers many bytes and the patch stream is nearly empty")
P[2][1].set_xlabel("byte position")
fig.suptitle("What ZSC actually stores.  bars = real bytes   red = the degree-3 curve   dotted = segment boundary\n"
             "lower strip = the patch (original byte minus the rounded curve value) — orange means a byte needed correcting",
             fontsize=12)
fig.savefig("/tmp/zsc_fit2.png",dpi=115,bbox_inches="tight")
print("saved")
