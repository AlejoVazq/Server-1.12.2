# -*- coding: utf-8 -*-
"""
Tema "Libro de aventuras" para Better Questing 3.5.329 + Standard Expansion 3.4.173.
Tapa de cuero con costura dorada y hojas de pergamino. Pixel art propio, sin librerías externas.

Uso:  python -I generar_tema_libro.py <carpeta resources/arremods>
Genera:
  <carpeta>/textures/gui/libro.png   atlas de 256x256
  <carpeta>/bq_themes.json           tema "arremods:libro" (hereda de bq_standard:light)

Las posiciones del atlas copian las del tema "light" de Standard Expansion, así el recorte en 9
partes (padding) funciona igual. Los marcos de los íconos de misión se toman del atlas original.
"""
import sys, os, zlib, struct, json, random

W = H = 256
img = [[(0, 0, 0, 0)] * W for _ in range(H)]
rnd = random.Random(1912)  # fijo: el atlas sale siempre igual

def hexc(s, a=255):
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)

CUERO_OSC = hexc("3A2010")
CUERO = hexc("6B3D1E")
CUERO_CLA = hexc("8A5430")
DORADO = hexc("C9A24A")
DORADO_OSC = hexc("8F6E2A")
PERG = hexc("EAD9AE")
PERG_CLA = hexc("F3E7C6")
PERG_OSC = hexc("D6BF8E")
TINTA = hexc("7A5A36")
TINTA_OSC = hexc("4E3520")

def put(x, y, c):
    img[y][x] = c

def ruido(c, amp):
    d = rnd.randint(-amp, amp)
    return tuple(max(0, min(255, c[i] + d)) for i in range(3)) + (c[3],)

def rect(x0, y0, w, h, c, amp=0):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            put(x, y, ruido(c, amp) if amp else c)

def borde(x0, y0, w, h, c, grosor=1):
    for g in range(grosor):
        for x in range(x0 + g, x0 + w - g):
            put(x, y0 + g, c); put(x, y0 + h - 1 - g, c)
        for y in range(y0 + g, y0 + h - g):
            put(x0 + g, y, c); put(x0 + w - 1 - g, y, c)

def esquinas_redondas(x0, y0, w, h):
    for (x, y) in ((x0, y0), (x0 + w - 1, y0), (x0, y0 + h - 1), (x0 + w - 1, y0 + h - 1)):
        put(x, y, (0, 0, 0, 0))

def costura(x0, y0, w, h, off):
    """Línea de puntadas doradas a 'off' píxeles del borde."""
    xa, ya, xb, yb = x0 + off, y0 + off, x0 + w - 1 - off, y0 + h - 1 - off
    for x in range(xa, xb + 1):
        if (x - xa) % 3 != 2:
            put(x, ya, DORADO); put(x, yb, DORADO)
    for y in range(ya, yb + 1):
        if (y - ya) % 3 != 2:
            put(xa, y, DORADO); put(xb, y, DORADO)

# --- panel_main [0,0,24,24] padding 8: tapa de cuero con costura + hoja de pergamino ---
rect(0, 0, 24, 24, CUERO, 10)
borde(0, 0, 24, 24, CUERO_OSC)
borde(1, 1, 22, 22, CUERO_CLA)
costura(0, 0, 24, 24, 3)
rect(7, 7, 10, 10, PERG, 6)          # la hoja empieza dentro del borde de 8 px
borde(7, 7, 10, 10, TINTA_OSC)        # canto de la hoja
rect(8, 8, 8, 8, PERG, 6)
esquinas_redondas(0, 0, 24, 24)

# --- aux_frame_0 [24,0,24,24] padding 8: recuadro de tinta sobre pergamino claro ---
rect(24, 0, 24, 24, PERG_CLA, 4)
borde(24, 0, 24, 24, TINTA)
borde(26, 2, 20, 20, PERG_OSC)
esquinas_redondas(24, 0, 24, 24)

# --- panel_inner [0,24,24,24] padding 8: hoja un poco más oscura con filete ---
rect(0, 24, 24, 24, PERG_OSC, 5)
borde(0, 24, 24, 24, TINTA)
esquinas_redondas(0, 24, 24, 24)

# --- item_frame [40,24,8,8] padding 1: casilla ---
rect(40, 24, 8, 8, PERG_OSC, 3)
borde(40, 24, 8, 8, TINTA)

# --- barras de desplazamiento ---
rect(24, 24, 16, 8, PERG_OSC, 3); borde(24, 24, 16, 8, TINTA)            # scroll_h_bg
rect(24, 32, 16, 8, CUERO, 8); borde(24, 32, 16, 8, CUERO_OSC)           # scroll_h knob
for x in range(27, 37): put(x, 33, CUERO_CLA)
rect(24, 40, 8, 16, PERG_OSC, 3); borde(24, 40, 8, 16, TINTA)            # scroll_v_bg
rect(32, 40, 8, 16, CUERO, 8); borde(32, 40, 8, 16, CUERO_OSC)           # scroll_v knob
for y in range(43, 53): put(33, y, CUERO_CLA)

# --- botones [40,32] apagado, [40,40] normal, [40,48] con el mouse encima; 8x8 padding 1 ---
def boton(x0, y0, fondo, filo, luz):
    rect(x0, y0, 8, 8, fondo, 3)
    borde(x0, y0, 8, 8, filo)
    for x in range(x0 + 1, x0 + 7): put(x, y0 + 1, luz)
boton(40, 32, hexc("BFB49A"), hexc("8C826C"), hexc("CFC5AD"))
boton(40, 40, hexc("D8BF8A"), CUERO, hexc("E8D3A2"))
boton(40, 48, hexc("F0DCA8"), DORADO_OSC, hexc("FFF0C8"))

# --- tooltip_bg [0,48,8,8] padding 2 ---
rect(0, 48, 8, 8, PERG_CLA, 2)
borde(0, 48, 8, 8, TINTA_OSC)
borde(1, 49, 6, 6, PERG_OSC)

# ---------------------------------------------------------------------------
def write_png(path):
    raw = b"".join(b"\x00" + b"".join(struct.pack("BBBB", *px) for px in row) for row in img)
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(path, "wb").write(png)

ATLAS = "arremods:textures/gui/libro.png"
ORIG = "bq_standard:textures/gui/gui_themes.png"

def tex(bounds, padding, mode, atlas=ATLAS):
    return {"textureType": "betterquesting:texture_sliced", "atlas": atlas,
            "bounds": bounds, "padding": padding, "sliceMode": mode}

def col(c):
    return {"colorType": "betterquesting:color_static", "color": c}

def pulso(a, b):
    return {"colorType": "betterquesting:color_pulse", "period": 1.0, "phase": 0.0, "color1": col(a), "color2": col(b)}

B = "betterquesting:"
textures = {
    B + "panel_main": tex([0, 0, 24, 24], [8, 8, 8, 8], 2),
    B + "aux_frame_0": tex([24, 0, 24, 24], [8, 8, 8, 8], 1),
    B + "panel_inner": tex([0, 24, 24, 24], [8, 8, 8, 8], 1),
    B + "item_frame": tex([40, 24, 8, 8], [1, 1, 1, 1], 2),
    B + "tooltip_bg": tex([0, 48, 8, 8], [2, 2, 2, 2], 1),
    B + "scroll_h_bg": tex([24, 24, 16, 8], [1, 1, 1, 1], 2),
    B + "scroll_v_bg": tex([24, 40, 8, 16], [1, 1, 1, 1], 2),
    B + "btn_normal_0": tex([40, 32, 8, 8], [1, 1, 1, 1], 1),
    B + "btn_normal_1": tex([40, 40, 8, 8], [1, 1, 1, 1], 1),
    B + "btn_normal_2": tex([40, 48, 8, 8], [1, 1, 1, 1], 1),
}
for i in range(3):
    textures[B + "scroll_h_%d" % i] = tex([24, 32, 16, 8], [4, 3, 4, 3], 2)
    textures[B + "scroll_v_%d" % i] = tex([32, 40, 8, 16], [3, 4, 3, 4], 2)
for i in range(4):  # marcos de los íconos: los del tema "light" original (se tiñen según el estado)
    textures[B + "quest_norm_%d" % i] = tex([0, 56, 24, 24], [8, 8, 8, 8], 1, ORIG)
    textures[B + "quest_main_%d" % i] = tex([24, 56, 24, 24], [11, 5, 11, 5], 1, ORIG)

TINTA_TXT = "FF3B2412"
colors = {
    B + "text_header": col(TINTA_TXT),
    B + "text_main": col(TINTA_TXT),
    B + "text_aux_0": col("FF5A4028"),
    B + "text_aux_1": col("FF7A5A36"),
    B + "text_highlight": col("FF8A2A10"),
    B + "text_watermark": col("807A5A36"),
    B + "gui_divider": col("FF7A5A36"),
    B + "grid_major": col("406B3D1E"),
    B + "grid_minor": col("206B3D1E"),
    B + "btn_idle": col(TINTA_TXT),
    B + "btn_disabled": col("FF8C826C"),
    B + "quest_line_locked": col("FF901010"),
    B + "quest_line_unlocked": pulso("FFB06000", "FF603000"),
    B + "quest_line_pending": col("FF207020"),
    B + "quest_line_complete": col("FF207020"),
    B + "quest_icon_locked": col("FF8C826C"),
    B + "quest_icon_unlocked": pulso("FFC07010", "FF704000"),
    B + "quest_icon_pending": pulso("FF00A0A0", "FF006060"),
    B + "quest_icon_complete": col("FF30A030"),
}

theme = [{"themeID": "arremods:libro", "themeName": "Libro de aventuras", "themeParent": "bq_standard:light",
          "textures": textures, "colors": colors}]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "textures", "gui"), exist_ok=True)
    write_png(os.path.join(out, "textures", "gui", "libro.png"))
    with open(os.path.join(out, "bq_themes.json"), "w", encoding="utf-8") as f:
        json.dump(theme, f, ensure_ascii=False, indent=2)
    print("ok", out)
