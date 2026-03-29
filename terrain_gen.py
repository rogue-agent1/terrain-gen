#!/usr/bin/env python3
"""Procedural terrain generator using diamond-square algorithm."""
import sys, random, math

def diamond_square(size, roughness=0.5, seed=42):
    random.seed(seed); n = size
    grid = [[0.0]*n for _ in range(n)]
    grid[0][0] = random.random(); grid[0][n-1] = random.random()
    grid[n-1][0] = random.random(); grid[n-1][n-1] = random.random()
    step = n - 1; scale = roughness
    while step > 1:
        half = step // 2
        for y in range(0, n-1, step):
            for x in range(0, n-1, step):
                avg = (grid[y][x]+grid[y][x+step]+grid[y+step][x]+grid[y+step][x+step])/4
                grid[y+half][x+half] = avg + (random.random()-0.5)*scale
        for y in range(0, n, half):
            for x in range((half if y % step == 0 else 0), n, step):
                vals = []
                if y >= half: vals.append(grid[y-half][x])
                if y+half < n: vals.append(grid[y+half][x])
                if x >= half: vals.append(grid[y][x-half])
                if x+half < n: vals.append(grid[y][x+half])
                grid[y][x] = sum(vals)/len(vals) + (random.random()-0.5)*scale
        step = half; scale *= 0.5
    return grid

def render_ascii(grid, w=80, h=40):
    n = len(grid); chars = "~.:-=+*#%@▲"
    mn = min(min(r) for r in grid); mx = max(max(r) for r in grid); rng = mx - mn or 1
    for y in range(min(h, n)):
        row = ""
        for x in range(min(w, n)):
            v = (grid[y][x] - mn) / rng
            row += chars[min(int(v * len(chars)), len(chars)-1)]
        print(row)

def render_colored(grid, w=80, h=40):
    n = len(grid)
    mn = min(min(r) for r in grid); mx = max(max(r) for r in grid); rng = mx - mn or 1
    for y in range(min(h, n)):
        row = ""
        for x in range(min(w, n)):
            v = (grid[y][x] - mn) / rng
            if v < 0.3: row += "\033[34m~\033[0m"
            elif v < 0.4: row += "\033[33m.\033[0m"
            elif v < 0.6: row += "\033[32m+\033[0m"
            elif v < 0.8: row += "\033[90m#\033[0m"
            else: row += "\033[37m▲\033[0m"
        print(row)

def stats(grid):
    flat = [v for row in grid for v in row]
    mn, mx, avg = min(flat), max(flat), sum(flat)/len(flat)
    water = sum(1 for v in flat if v < mn + (mx-mn)*0.3) / len(flat)
    return f"Size: {len(grid)}x{len(grid)}, Range: [{mn:.2f}, {mx:.2f}], Avg: {avg:.2f}, Water: {water:.0%}"

def main():
    import argparse
    p = argparse.ArgumentParser(description="Terrain generator")
    p.add_argument("-s", "--size", type=int, default=65)
    p.add_argument("-r", "--roughness", type=float, default=0.6)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--color", action="store_true")
    args = p.parse_args()
    size = args.size
    if size & (size-1) != 0 or size < 3: size = 2**int(math.log2(max(size-1,2))) + 1
    grid = diamond_square(size, args.roughness, args.seed)
    print(f"=== Terrain ({stats(grid)}) ===\n")
    if args.color: render_colored(grid)
    else: render_ascii(grid)

if __name__ == "__main__": main()
