import numpy as np, math, lzma, sys
sys.path.insert(0,"/tmp/src")
from zsc_lossless import ZSCLossless
c=ZSCLossless(); rng=np.random.default_rng(7)
def run(name, arr, note=""):
    raw=arr.astype(np.uint8).tobytes()
    pl,order=c.compress(arr,container="lzma"); pa,_=c.compress(arr,container="none")
    ok=np.array_equal(c.decompress(pl),arr.astype(np.uint8))
    xz=len(raw)/len(lzma.compress(raw,preset=9))
    print("%-34s %9.2fx %10.2fx %8.2fx  %-7s %s"
          %(name,len(raw)/len(pa),len(raw)/len(pl),xz,order,note))
    return ok

print("%-34s %9s %10s %8s  %-7s"%("game data","addressable","sequential","xz -9","order")); print("-"*84)

# terrain heightmap: fractal noise, the classic smooth 2-D field
h=np.zeros((256,256))
for oct in range(5):
    f=2**oct; a=1.0/f
    g=rng.standard_normal((f+2,f+2))
    yy,xx=np.mgrid[0:256,0:256]
    h+=a*np.cos(xx*f*math.pi/256+g[0,0])*np.cos(yy*f*math.pi/256+g[0,1])
run("terrain heightmap 256x256", np.clip((h-h.min())/(h.max()-h.min())*255,0,255).astype(np.uint8))

# light propagation field: smooth, 0..15, the shape Minecraft actually stores
S=32
g3=np.stack(np.meshgrid(*[np.arange(S)]*3,indexing="ij"),0).astype(float)
d=np.sqrt(sum((g3[a]-16)**2 for a in range(3)))
run("light field 32^3 (0..15)", np.clip(15-d/2.5,0,15).astype(np.uint8), "values 0..15")

# block IDs: categorical, spatially clustered, layered in Y - a Minecraft chunk
S=32
blocks=np.zeros((S,S,S),dtype=np.uint8)
for y in range(S):
    if y<8: blocks[:,y,:]=1        # bedrock/stone
    elif y<14: blocks[:,y,:]=3     # dirt
    elif y<15: blocks[:,y,:]=2     # grass
    else: blocks[:,y,:]=0          # air
blocks[rng.random((S,S,S))<0.02]=16   # scattered ore
run("minecraft-ish chunk 32^3", blocks, "block IDs are CATEGORICAL")

# the same chunk over 16 ticks, barely changing - what a server actually stores
seq=np.repeat(blocks[...,None],16,axis=3).copy()
for t in range(1,16):
    for _ in range(20):
        x,y,z=rng.integers(0,S,3); seq[x,y,z,t:]=0     # a player mining
run("chunk x 16 ticks (edits only)", seq, "temporal coherence")

# physics: 64 entities, 3 coords, over 256 ticks - smooth in time
P=np.zeros((64,3,256))
for i in range(64):
    v=rng.standard_normal(3)*0.3; p=rng.random(3)*200
    for t in range(256):
        p=p+v; v+=rng.standard_normal(3)*0.02
        P[i,:,t]=np.clip(p%255,0,255)
run("entity positions 64x3x256", P.astype(np.uint8), "smooth in time")
