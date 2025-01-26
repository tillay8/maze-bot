import random, time
from PIL import Image

Scale = 10
SIDE, START, PATH, END = (0, 228, 48), (255, 0, 0), (0, 121, 241), (0, 0, 0)

def export(num):
    W, H = num, num
    field = [0] * (W * H)
    createMaze(field, W, H)
    return createImage("maze.png", field, W, H)

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
        if isPossible(field, up, 1, W, H): possible.append(up)
        if isPossible(field, down, 1, W, H): possible.append(down)
        if isPossible(field, left, 1, W, H): possible.append(left)
        if isPossible(field, right, 1, W, H): possible.append(right)
        if not possible:
            if not history: return
            pos = history.pop()
            continue
        history.append(pos)
        pos = random.choice(possible)
        field[pos[1] * W + pos[0]] = 1
        fill(field, history[-1], pos, W)

def fill(field, o, n, W):
    if o[0] != n[0]:
        field[((n[0] - o[0]) // 2) + o[1] * W + o[0]] = 1
    else:
        field[((n[1] - o[1]) // 2 + o[1]) * W + o[0]] = 1

def createImage(file, field, W, H):
    img = Image.new("RGB", (W * Scale, H * Scale), PATH)
    pixels = img.load()
    for x in range(W):
        for y in range(H):
            c = SIDE if field[x + y * W] == 0 else PATH
            for i in range(Scale):
                for j in range(Scale):
                    pixels[x * Scale + i, y * Scale + j] = c
    for i in range(Scale):
        for j in range(Scale):
            pixels[i, j] = START
    for i in range(Scale):
        for j in range(Scale):
            pixels[(W - 1) * Scale + i, (H - 1) * Scale + j] = END
    img.save(file)
    return file

export(127)
