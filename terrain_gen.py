import argparse, random

def diamond_square(size, roughness=0.5, seed=None):
    if seed: random.seed(seed)
    n = size
    grid = [[0.0]*n for _ in range(n)]
    grid[0][0] = random.random()
    grid[0][n-1] = random.random()
    grid[n-1][0] = random.random()
    grid[n-1][n-1] = random.random()
    step = n - 1
    scale = roughness
    while step > 1:
        half = step // 2
        # Diamond
        for y in range(0, n-1, step):
            for x in range(0, n-1, step):
                avg = (grid[y][x] + grid[y][x+step] + grid[y+step][x] + grid[y+step][x+step]) / 4
                grid[y+half][x+half] = avg + random.uniform(-scale, scale)
        # Square
        for y in range(0, n, half):
            for x in range((y+half) % step, n, step):
                vals = []
                if y-half >= 0: vals.append(grid[y-half][x])
                if y+half < n: vals.append(grid[y+half][x])
                if x-half >= 0: vals.append(grid[y][x-half])
                if x+half < n: vals.append(grid[y][x+half])
                grid[y][x] = sum(vals)/len(vals) + random.uniform(-scale, scale)
        step = half
        scale *= 0.5
    return grid

def display(grid, chars=" ·~≈░▒▓█"):
    mn = min(min(r) for r in grid)
    mx = max(max(r) for r in grid)
    rng = mx - mn or 1
    for row in grid:
        print("".join(chars[min(int((v-mn)/rng*(len(chars)-1)), len(chars)-1)] for v in row))

def main():
    p = argparse.ArgumentParser(description="Terrain generator")
    p.add_argument("-s", "--size", type=int, default=33, help="Must be 2^n+1")
    p.add_argument("-r", "--roughness", type=float, default=0.5)
    p.add_argument("--seed", type=int)
    p.add_argument("--height-map", action="store_true")
    args = p.parse_args()
    grid = diamond_square(args.size, args.roughness, args.seed)
    if args.height_map:
        for row in grid:
            print(" ".join(f"{v:.2f}" for v in row))
    else:
        display(grid)

if __name__ == "__main__":
    main()
