#!/usr/bin/env python3
"""terrain_gen - 2D terrain map generator."""
import sys, random, hashlib, math
def noise(x, y, seed=42):
    h=int(hashlib.md5(f"{x},{y},{seed}".encode()).hexdigest()[:8],16)
    return h/0xFFFFFFFF
def smooth_noise(x, y, seed=42):
    x0,y0=int(math.floor(x)),int(math.floor(y))
    fx,fy=x-x0,y-y0; fx=fx*fx*(3-2*fx); fy=fy*fy*(3-2*fy)
    n00,n10=noise(x0,y0,seed),noise(x0+1,y0,seed)
    n01,n11=noise(x0,y0+1,seed),noise(x0+1,y0+1,seed)
    return (n00*(1-fx)+n10*fx)*(1-fy)+(n01*(1-fx)+n11*fx)*fy
def terrain(x, y, seed=42):
    v=0; amp=1; freq=1; total_amp=0
    for _ in range(5):
        v+=smooth_noise(x*freq*0.05,y*freq*0.05,seed)*amp
        total_amp+=amp; amp*=0.5; freq*=2
    return v/total_amp
BIOMES = {0.2:"~",0.3:".",0.5:",",0.65:'"',0.75:"t",0.85:"T",0.95:"^",1.0:"#"}
def get_biome(v):
    for threshold, char in sorted(BIOMES.items()):
        if v<=threshold: return char
    return "#"
if __name__=="__main__":
    w=int(sys.argv[1]) if len(sys.argv)>1 else 60
    h=int(sys.argv[2]) if len(sys.argv)>2 else 25
    seed=int(sys.argv[3]) if len(sys.argv)>3 else random.randint(0,9999)
    print(f"Seed: {seed}")
    for r in range(h):
        print("".join(get_biome(terrain(c,r,seed)) for c in range(w)))
    print("~ water  . sand  , grass  \" meadow  t tree  T forest  ^ mountain  # peak")
