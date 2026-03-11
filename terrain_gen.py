#!/usr/bin/env python3
"""Terrain generator — diamond-square algorithm for heightmap generation."""
import sys, random

def diamond_square(size=65, roughness=0.8, seed=42):
    random.seed(seed)
    n = size
    grid = [[0.0]*n for _ in range(n)]
    grid[0][0] = grid[0][n-1] = grid[n-1][0] = grid[n-1][n-1] = 0.5
    step = n - 1
    scale = roughness
    while step > 1:
        half = step // 2
        # Diamond step
        for y in range(0, n-1, step):
            for x in range(0, n-1, step):
                avg = (grid[y][x] + grid[y][x+step] + grid[y+step][x] + grid[y+step][x+step]) / 4
                grid[y+half][x+half] = avg + random.uniform(-scale, scale)
        # Square step
        for y in range(0, n, half):
            for x in range((half if y % step == 0 else 0), n, step):
                pts = []
                if y >= half: pts.append(grid[y-half][x])
                if y + half < n: pts.append(grid[y+half][x])
                if x >= half: pts.append(grid[y][x-half])
                if x + half < n: pts.append(grid[y][x+half])
                grid[y][x] = sum(pts)/len(pts) + random.uniform(-scale, scale)
        step = half
        scale *= 0.5
    return grid

def render(grid, w=80, h=30):
    n = len(grid)
    biomes = [("~", "water"), (".", "sand"), (",", "grass"), (":", "forest"), ("^", "mountain"), ("▲", "peak")]
    for row in range(h):
        line = ""
        for col in range(w):
            gy = int(row / h * n) % n
            gx = int(col / w * n) % n
            v = max(0, min(1, (grid[gy][gx] + 1) / 2))
            idx = min(len(biomes)-1, int(v * len(biomes)))
            line += biomes[idx][0]
        print(line)

if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 65
    # Ensure size is 2^n + 1
    import math
    p = max(2, int(math.log2(size-1)) if size > 2 else 2)
    size = 2**p + 1
    grid = diamond_square(size)
    print(f"Terrain: {size}x{size} heightmap\n")
    render(grid)
