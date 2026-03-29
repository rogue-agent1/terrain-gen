#!/usr/bin/env python3
"""Terrain Generator - Diamond-square algorithm for heightmap generation."""
import sys, random

def diamond_square(size, roughness=0.5, seed=42):
    random.seed(seed)
    n = size; grid = [[0.0]*n for _ in range(n)]
    grid[0][0] = random.random(); grid[0][n-1] = random.random()
    grid[n-1][0] = random.random(); grid[n-1][n-1] = random.random()
    step = n - 1; scale = roughness
    while step > 1:
        half = step // 2
        for y in range(half, n, step):
            for x in range(half, n, step):
                avg = (grid[y-half][x-half] + grid[y-half][x+half if x+half<n else x] +
                       grid[y+half if y+half<n else y][x-half] + grid[y+half if y+half<n else y][x+half if x+half<n else x]) / 4
                grid[y][x] = avg + random.uniform(-scale, scale)
        for y in range(0, n, half):
            for x in range((half if y % step == 0 else 0), n, step):
                pts = []
                if y >= half: pts.append(grid[y-half][x])
                if y + half < n: pts.append(grid[y+half][x])
                if x >= half: pts.append(grid[y][x-half])
                if x + half < n: pts.append(grid[y][x+half])
                grid[y][x] = sum(pts)/len(pts) + random.uniform(-scale, scale)
        scale *= 0.5
    return grid

def render(grid, width=65, height=25):
    biomes = [("~", "water"), (".", "sand"), (",", "grass"), ("^", "hill"), ("#", "mountain"), ("A", "peak")]
    rows = len(grid); cols = len(grid[0])
    mn = min(min(r) for r in grid); mx = max(max(r) for r in grid); rng = mx - mn or 1
    lines = []
    sy = max(1, rows // height); sx = max(1, cols // width)
    for y in range(0, min(rows, height*sy), sy):
        row = ""
        for x in range(0, min(cols, width*sx), sx):
            v = (grid[y][x] - mn) / rng
            idx = min(len(biomes)-1, int(v * len(biomes)))
            row += biomes[idx][0]
        lines.append(row)
    return "\n".join(lines)

def main():
    size = 65; roughness = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    grid = diamond_square(size, roughness, seed)
    print(f"=== Terrain Generator ({size}x{size}, roughness={roughness}) ===\n")
    print(render(grid))
    print("\nLegend: ~water .sand ,grass ^hill #mountain Apeak")

if __name__ == "__main__":
    main()
