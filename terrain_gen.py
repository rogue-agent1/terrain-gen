#!/usr/bin/env python3
"""terrain_gen - Procedural terrain with erosion."""
import argparse, math, random, sys

class Perlin:
    def __init__(self, seed=0):
        random.seed(seed)
        self.p = list(range(256)); random.shuffle(self.p); self.p *= 2
    def _fade(self, t): return t*t*t*(t*(t*6-15)+10)
    def _lerp(self, a,b,t): return a+t*(b-a)
    def _grad(self, h, x, y):
        h &= 3
        if h==0: return x+y
        if h==1: return -x+y
        if h==2: return x-y
        return -x-y
    def noise(self, x, y):
        xi, yi = int(x)&255, int(y)&255
        xf, yf = x-int(x), y-int(y)
        u, v = self._fade(xf), self._fade(yf)
        aa=self.p[self.p[xi]+yi]; ab=self.p[self.p[xi]+yi+1]
        ba=self.p[self.p[xi+1]+yi]; bb=self.p[self.p[xi+1]+yi+1]
        return self._lerp(
            self._lerp(self._grad(aa,xf,yf), self._grad(ba,xf-1,yf), u),
            self._lerp(self._grad(ab,xf,yf-1), self._grad(bb,xf-1,yf-1), u), v)
    def octave(self, x, y, octaves=6, persistence=0.5):
        total=0; freq=1; amp=1; mx=0
        for _ in range(octaves):
            total += self.noise(x*freq, y*freq)*amp
            mx += amp; freq *= 2; amp *= persistence
        return total/mx

def erode(heightmap, w, h, iterations=5000):
    random.seed(42)
    for _ in range(iterations):
        x, y = random.uniform(1,w-2), random.uniform(1,h-2)
        sediment = 0; speed = 1; water = 1
        for _ in range(30):
            ix, iy = int(x), int(y)
            if ix<1 or ix>=w-1 or iy<1 or iy>=h-1: break
            # Gradient
            gx = heightmap[iy][ix+1]-heightmap[iy][ix-1]
            gy = heightmap[iy+1][ix]-heightmap[iy-1][ix]
            l = math.sqrt(gx*gx+gy*gy) or 1
            x -= gx/l; y -= gy/l
            nix, niy = int(x), int(y)
            if nix<0 or nix>=w or niy<0 or niy>=h: break
            dh = heightmap[niy][nix] - heightmap[iy][ix]
            capacity = max(-dh, 0.01) * speed * water
            if sediment > capacity:
                deposit = (sediment-capacity)*0.3
                heightmap[iy][ix] += deposit; sediment -= deposit
            else:
                erode_amt = min((capacity-sediment)*0.3, -dh)
                heightmap[iy][ix] -= erode_amt; sediment += erode_amt
            speed = math.sqrt(max(speed*speed-dh, 0.01))
            water *= 0.99

def main():
    p = argparse.ArgumentParser(description="Terrain generator")
    p.add_argument("-W","--width",type=int,default=80)
    p.add_argument("-H","--height",type=int,default=40)
    p.add_argument("-s","--seed",type=int,default=42)
    p.add_argument("-e","--erode",type=int,default=3000)
    a = p.parse_args()
    pn = Perlin(a.seed)
    hmap = [[pn.octave(x*0.03, y*0.03) for x in range(a.width)] for y in range(a.height)]
    if a.erode: erode(hmap, a.width, a.height, a.erode)
    # Render with elevation colors
    chars = "~.,-:;=+*#%@"  # water to mountain
    for row in hmap:
        mn, mx = min(min(r) for r in hmap), max(max(r) for r in hmap)
        line = ""
        for v in row:
            nv = (v-mn)/(mx-mn) if mx>mn else 0.5
            ci = min(len(chars)-1, int(nv*(len(chars)-1)))
            line += chars[ci]
        print(line)

if __name__ == "__main__": main()
