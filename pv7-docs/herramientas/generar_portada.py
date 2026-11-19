# -*- coding: utf-8 -*-
"""
Portada del libro de misiones de ArreMods (pixel art original, sin librerías externas).
Uso: python -I generar_portada.py <salida.png>

Formato que espera Better Questing 3.5.329 (leído de GuiHome):
  - textura cuadrada; en coordenadas de 256x256:
    (0,0)-(256,128)   = fondo de la pantalla del libro
    (0,128)-(256,256) = logo (se dibuja respetando proporción, con transparencia)
  Acá se genera a 512x512 (el doble), igual que la imagen original del mod.
"""
import sys, zlib, struct, math, random

W = H = 512
img = [[(0, 0, 0, 0)] * W for _ in range(H)]

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img[y][x] = c

def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(len(a)))

def grad(stops, t):
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0) if t1 > t0 else 0)
    return stops[-1][1]

# ---------------------------------------------------------------------------
# FONDO: escena pixel art a 128x64, escalada x4 -> 512x256
# ---------------------------------------------------------------------------
PW, PH, S = 128, 64, 4
rnd = random.Random(7)
scene = [[None] * PW for _ in range(PH)]

sky = [(0.0, (18, 10, 48)), (0.35, (64, 22, 92)), (0.62, (176, 52, 96)),
       (0.80, (244, 120, 64)), (1.0, (255, 196, 92))]
BANDS = 14  # cielo en bandas (look pixel art)
for y in range(PH):
    t = min(1.0, y / 46.0)
    t = round(t * BANDS) / BANDS
    for x in range(PW):
        scene[y][x] = grad(sky, t)

# estrellas arriba
for _ in range(70):
    x, y = rnd.randrange(PW), rnd.randrange(0, 22)
    b = rnd.choice([150, 190, 235])
    scene[y][x] = (b, b, min(255, b + 20))

# sol poniente grande con franjas
cx, cy, r = 92, 38, 15
for y in range(PH):
    for x in range(PW):
        d = math.hypot(x - cx, y - cy)
        if d <= r:
            t = (y - (cy - r)) / (2 * r)
            col = grad([(0, (255, 236, 150)), (0.6, (255, 170, 70)), (1, (240, 90, 60))], t)
            if y > cy and (y - cy) % 4 in (0, 1) and (y - cy) > 2:  # franjas retro
                continue
            scene[y][x] = col
        elif d <= r + 2.5 and y < cy + 4:
            base = scene[y][x]
            scene[y][x] = lerp(base, (255, 200, 120), 0.35)

def ridge(base, amp, freq, seed, col, cap=None, trees=False):
    rr = random.Random(seed)
    ph = [rr.uniform(0, 6.28) for _ in range(3)]
    for x in range(PW):
        h = base - amp * (0.55 * math.sin(x * freq + ph[0]) + 0.3 * math.sin(x * freq * 2.3 + ph[1])
                          + 0.15 * math.sin(x * freq * 5.1 + ph[2]))
        top = int(h)
        for y in range(max(0, top), PH):
            scene[y][x] = col
        if cap and top >= 0:
            for k in range(2):
                if 0 <= top + k < PH:
                    scene[top + k][x] = cap
        if trees and rr.random() < 0.22 and top > 3:
            th = rr.randint(3, 6)
            for k in range(th):
                yy = top - k
                w = max(0, (th - k) // 2)
                for dx in range(-w, w + 1):
                    if 0 <= x + dx < PW and 0 <= yy < PH:
                        scene[yy][x + dx] = col

ridge(36, 9, 0.07, 1, (92, 34, 96), cap=(150, 70, 130))          # montañas lejanas
ridge(44, 7, 0.10, 2, (58, 22, 70), cap=(96, 40, 104))           # montañas medias
ridge(52, 4, 0.16, 3, (30, 12, 40), trees=True)                  # bosque cercano
ridge(59, 2, 0.25, 4, (16, 8, 24))                               # suelo

# lago con reflejo del sol
for y in range(56, 61):
    for x in range(70, 116):
        if abs(x - 93) < 22 - (y - 56) * 2:
            refl = (255, 150, 80) if (x + y) % 3 else (255, 210, 120)
            scene[y][x] = refl if abs(x - 92) < 8 - (y - 56) else (70, 40, 110)

# isla flotante con cascada (guiño a las dimensiones)
isl = [(22, 16, 14)]
for (ix, iy, iw) in isl:
    for k in range(7):
        w = iw - k * 2
        for dx in range(-w // 2, w // 2 + 1):
            yy = iy + k
            scene[yy][ix + dx] = (60, 40, 50) if k else (90, 200, 110)
    for dx in range(-iw // 2, iw // 2 + 1):
        scene[iy - 1][ix + dx] = (60, 170, 90)
    for k in range(4):  # arbolito
        scene[iy - 2 - k][ix - 3] = (40, 120, 70)
    for dx in (-5, -4, -2, -1):
        scene[iy - 5][ix + dx] = (40, 140, 80)
    for k in range(7, 34):  # cascada
        if iy + k < PH:
            scene[iy + k][ix + 4] = (120, 200, 255) if k % 3 else (200, 240, 255)

for y in range(PH):
    for x in range(PW):
        r_, g_, b_ = scene[y][x]
        for dy in range(S):
            for dx in range(S):
                put(x * S + dx, y * S + dy, (r_, g_, b_, 255))

# viñeta suave en el borde inferior del fondo
for y in range(236, 256):
    a = (y - 236) / 20.0
    for x in range(W):
        r_, g_, b_, _ = img[y][x]
        img[y][x] = (int(r_ * (1 - 0.5 * a)), int(g_ * (1 - 0.5 * a)), int(b_ * (1 - 0.5 * a)), 255)

# ---------------------------------------------------------------------------
# LOGO "ARREMODS" en letras de bloque (franja y 256..383), fondo transparente
# ---------------------------------------------------------------------------
FONT = {
    'A': ["01110", "11011", "11011", "11111", "11011", "11011", "11011"],
    'R': ["11110", "11011", "11011", "11110", "11011", "11011", "11011"],
    'E': ["11111", "11000", "11000", "11110", "11000", "11000", "11111"],
    'M': ["11011", "11111", "11111", "10101", "10001", "10001", "10001"],
    'O': ["01110", "11011", "11011", "11011", "11011", "11011", "01110"],
    'D': ["11110", "11011", "11011", "11011", "11011", "11011", "11110"],
    'S': ["01111", "11000", "11000", "01110", "00011", "00011", "11110"],
}
SMALL = {  # 3x5 para el subtítulo
    'G': ["111", "100", "101", "101", "111"], 'U': ["101", "101", "101", "101", "111"],
    'I': ["111", "010", "010", "010", "111"], 'A': ["010", "101", "111", "101", "101"],
    'D': ["110", "101", "101", "101", "110"], 'E': ["111", "100", "110", "100", "111"],
    'V': ["101", "101", "101", "101", "010"], 'N': ["101", "111", "111", "111", "101"],
    'T': ["111", "010", "010", "010", "010"], 'R': ["110", "101", "110", "101", "101"],
    'S': ["111", "100", "111", "001", "111"], ' ': ["000", "000", "000", "000", "000"],
}

def text_cells(txt, font, w):
    cells = []
    cx = 0
    for ch in txt:
        g = font[ch]
        for gy, row in enumerate(g):
            for gx, v in enumerate(row):
                if v == '1':
                    cells.append((cx + gx, gy))
        cx += w + 1
    return cells, cx - 1

word, ww = text_cells("ARREMODS", FONT, 5)
CELL = 10
ox = (W - ww * CELL) // 2
oy = 268
mask = set()
for (gx, gy) in word:
    for dy in range(CELL):
        for dx in range(CELL):
            mask.add((ox + gx * CELL + dx, oy + gy * CELL + dy))

# sombra
for (x, y) in mask:
    for d in range(1, 7):
        if (x + d, y + d) not in mask:
            put(x + d, y + d, (20, 6, 28, 255))
# contorno
OUT = 4
for (x, y) in list(mask):
    for dy in range(-OUT, OUT + 1):
        for dx in range(-OUT, OUT + 1):
            p = (x + dx, y + dy)
            if p not in mask and 0 <= p[0] < W and 0 <= p[1] < H:
                put(p[0], p[1], (34, 10, 44, 255))
# relleno degradado dorado con brillo y textura de bloque
top_y, bot_y = oy, oy + 7 * CELL
for (x, y) in mask:
    t = (y - top_y) / float(bot_y - top_y)
    col = grad([(0, (255, 246, 170)), (0.45, (255, 196, 60)), (0.55, (235, 140, 30)), (1, (190, 70, 20))], t)
    lx, ly = (x - ox) % CELL, (y - oy) % CELL
    if lx == 0 or ly == 0:              # bisel claro arriba/izquierda de cada bloque
        col = lerp(col, (255, 255, 230), 0.35)
    elif lx == CELL - 1 or ly == CELL - 1:  # bisel oscuro
        col = lerp(col, (120, 40, 10), 0.35)
    put(x, y, col + (255,))

# subtítulo
sub, sw = text_cells("GUIA DE AVENTURAS", SMALL, 3)
SC = 4
sx = (W - sw * SC) // 2
sy = oy + 7 * CELL + 16
smask = set()
for (gx, gy) in sub:
    for dy in range(SC):
        for dx in range(SC):
            smask.add((sx + gx * SC + dx, sy + gy * SC + dy))
for (x, y) in smask:
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            if (x + dx, y + dy) not in smask:
                put(x + dx, y + dy, (34, 10, 44, 255))
for (x, y) in smask:
    put(x, y, (190, 235, 255, 255))

# ---------------------------------------------------------------------------
def write_png(path):
    raw = b''.join(b'\x00' + bytes(v for px in row for v in px) for row in img)
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(png)

write_png(sys.argv[1])
print('ok', sys.argv[1])
