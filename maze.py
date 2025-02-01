import random
import time
from PIL import Image

# Maze colors
SIDE, START, PATH, END = (0, 0, 0), (255, 0, 0), (255, 255, 255), (0, 0, 255)

def export(num, create):
    start_time = time.time()
    W, H = int(num), int(num)
    if W < 100:
        Scale = 10 
    elif W < 200:
        Scale = 5
    else:
        Scale = 1
    field = [0] * (W * H)
    createMaze(field, W, H)
    end_time = time.time()
    print(f"Time to generate and path maze: {end_time - start_time:.2f} seconds")

    return createImage("maze.png", field, W, H, create, Scale)

def isPossible(field, p, val, W, H):
    if p[0] < 0 or p[1] < 0 or p[0] >= W or p[1] >= H:
        return False
    return field[p[1] * W + p[0]] != val if val == 1 else field[p[1] * W + p[0]] == 1

def createDirections(p, s):
    return (p[0], p[1] - s), (p[0], p[1] + s), (p[0] - s, p[1]), (p[0] + s, p[1])

def createMaze(field, W, H):
    random.seed(time.time())
    history, pos = [], (0, 0)
    while True:
        possible = []
        up, down, left, right = createDirections(pos, 2)
        if isPossible(field, up, 1, W, H): 
            possible.append(up)
        if isPossible(field, down, 1, W, H): 
            possible.append(down)
        if isPossible(field, left, 1, W, H): 
            possible.append(left)
        if isPossible(field, right, 1, W, H): 
            possible.append(right)
        if not possible:
            if not history: return
            pos = history.pop()
            continue
        history.append(pos)
        pos = random.choice(possible)
        field[pos[1] * W + pos[0]] = 1
        fill(field, history[-1], pos, W)
    print("finished pathing maze")

def fill(field, o, n, W):
    if o[0] != n[0]:
        field[((n[0] - o[0]) // 2) + o[1] * W + o[0]] = 1
    else:
        field[((n[1] - o[1]) // 2 + o[1]) * W + o[0]] = 1

def createImage(file, field, W, H, create, Scale):
    img = Image.new("RGB", ((W + 2) * Scale, (H + 2) * Scale), SIDE)
    pixels = img.load()
    print(f"scale: {Scale} size: {W}")
    for x in range(W):
        for y in range(H):
            c = SIDE if field[x + y * W] == 0 else PATH
            for i in range(Scale):
                for j in range(Scale):
                    pixels[(x + 1) * Scale + i, (y + 1) * Scale + j] = c
                    progress = ((x * H + y) * Scale * Scale + i * Scale + j) / (W * H * Scale * Scale) * 100
                    print(f"\rgenerating image: {progress:.2f}%", end="")
    for i in range(Scale):
        for j in range(Scale):
            pixels[i+Scale, j+Scale] = START
    for i in range(Scale):
        for j in range(Scale):
            pixels[(W) * Scale + i, (H) * Scale + j] = END
    print("\nexporting image...")
    img.save(file)
    print(f"saved image to working directory")
    return file