#!/usr/bin/env python3
"""Procedural terrain with diamond-square algorithm."""
import sys, random, math

def diamond_square(size, roughness=0.5):
    n = size; grid = [[0.0]*n for _ in range(n)]
    grid[0][0] = random.random(); grid[0][n-1] = random.random()
    grid[n-1][0] = random.random(); grid[n-1][n-1] = random.random()
    step = n - 1; scale = roughness
    while step > 1:
        half = step // 2
        for y in range(0, n-1, step):
            for x in range(0, n-1, step):
                avg = (grid[y][x]+grid[y][x+step]+grid[y+step][x]+grid[y+step][x+step])/4
                grid[y+half][x+half] = avg + random.uniform(-scale, scale)
        for y in range(0, n, half):
            for x in range((half if y%step==0 else 0), n, step):
                total = count = 0
                for dy, dx in [(-half,0),(half,0),(0,-half),(0,half)]:
                    ny, nx = y+dy, x+dx
                    if 0<=ny<n and 0<=nx<n: total += grid[ny][nx]; count += 1
                grid[y][x] = total/count + random.uniform(-scale, scale)
        step = half; scale *= 0.5
    return grid

def main():
    random.seed(42); n = 33; grid = diamond_square(n, 0.6)
    biomes = " ~≈░▒▓█▲"  # water, sand, grass, forest, mountain, snow
    print(f"Terrain ({n}x{n}):")
    for y in range(0, n, 2):
        row = ""
        for x in range(0, n):
            v = grid[y][x]; level = max(0, min(int((v+1)*4), len(biomes)-1))
            row += biomes[level]
        print(row)

if __name__ == "__main__": main()
