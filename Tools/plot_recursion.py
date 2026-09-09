import numpy as np, torch, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
BG="#12151c"; FG="#dfe6f0"; GRID="#2b3240"
plt.rcParams.update({"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,
    "text.color":FG,"axes.labelcolor":FG,"xtick.color":FG,"ytick.color":FG,
    "axes.edgecolor":GRID,"grid.color":GRID,"axes.titlecolor":FG,"font.size":10})
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

N=2048
sig=np.frombuffer(open("/samples/smooth_1d.bin","rb").read()[:N],dtype=np.uint8)
sl,coef,orig=zsc(sig,0.004)
patch=np.zeros(N)
for k,(s,e) in enumerate(sl):
    if s>=N: continue
    L=e-s; x=np.linspace(-1,1,L)
    A=np.stack([np.ones_like(x),x,2*x**2-1,4*x**3-3*x],1)
    rec=np.clip((A@coef[k])*255.0,0,255).round()
    patch[s:min(e,N)]=orig[s:min(e,N)].round()-rec[:min(e,N)-s]

fig,ax=plt.subplots(3,1,figsize=(14,9))
ax[0].plot(orig[:N],color="#7fb2ff",lw=1.0,label="original bytes")
for s,e in sl:
    if s>=N: continue
    L=e-s; x=np.linspace(-1,1,L)
    A=np.stack([np.ones_like(x),x,2*x**2-1,4*x**3-3*x],1)
ax[0].plot([np.nan],[np.nan])
rec_full=orig-patch
ax[0].plot(rec_full[:N],color="#ff6b8a",lw=1.2,ls="--",label="what ZSC stores (the curves)")
ax[0].legend(facecolor=BG,edgecolor=GRID,labelcolor=FG); ax[0].set_ylabel("byte value")
ax[0].set_title("pass 1: the fit takes the slow-moving part",loc="left")

ax[1].plot(patch[:N],color="#ffb454",lw=0.9)
ax[1].set_ylabel("patch"); ax[1].set_xlabel("byte position")
ax[1].set_title("what is left over — the patch stream ZSC would have to compress on a second pass",loc="left")

f=np.fft.rfftfreq(N); 
so=np.abs(np.fft.rfft(orig[:N]-orig[:N].mean())); sp=np.abs(np.fft.rfft(patch[:N]-patch[:N].mean()))
ax[2].semilogy(f,so+1e-6,color="#7fb2ff",lw=1.0,label="original")
ax[2].semilogy(f,sp+1e-6,color="#ffb454",lw=1.0,label="patch stream")
ax[2].set_xlabel("frequency (cycles per sample)"); ax[2].set_ylabel("magnitude")
ax[2].legend(facecolor=BG,edgecolor=GRID,labelcolor=FG)
ax[2].set_title("why a second pass finds nothing: the fit removed the low frequencies, "
                "and the leftover is flat across the spectrum",loc="left")
for a in ax: a.grid(alpha=0.25)
fig.suptitle("Running ZSC on its own patch stream",fontsize=13)
fig.tight_layout(rect=[0,0,1,0.96])
fig.savefig("/tmp/zsc_recursion.png",dpi=115)
print("saved")
