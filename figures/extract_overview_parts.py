"""Crop all assets for the redesigned 'VISAtlas System Overview' slide.

Sources (VISAtlas paper PDF):
  p4  Fig. 1 : synthetic chart (Training), CNN, prediction pie + vector
  p12 Fig.10 : real-world chart thumbnails (Beagle pie/donut row)
  p4  Fig. 1 : Embedding Overview / Histogram / Gallery panels
"""

import pymupdf
from PIL import Image, ImageDraw

SRC = "/mnt/c/Users/Administrator/Downloads/VISAtlas (1).pdf"
OUT = "/home/yaojunhe/va-talk/figures/%s.png"
DPI = 500

CROPS = {
    # name: (page, clip)
    "left_synthetic": (3, (425.5, 75.0, 438.2, 87.4)),
    "left_real1":     (11, (315.5, 166.5, 342.3, 193.3)),
    "left_real2":     (11, (488.3, 166.5, 515.1, 193.3)),
    "left_real3":     (11, (429.7, 166.5, 457.5, 193.3)),
    "center_input":   (3, (424.2, 106.8, 443.6, 128.6)),
    "center_cnn":     (3, (457.5, 66.0, 478.5, 91.0)),
    "center_vector":  (3, (491.8, 106.9, 516.5, 129.4)),
    "right_explore":  (3, (303.0, 165.2, 413.2, 247.0)),
    "right_compare":  (3, (416.2, 170.4, 534.6, 198.3)),
    "right_query":    (3, (416.2, 218.9, 534.6, 249.8)),
}

doc = pymupdf.open(SRC)
tiles = []
for name, (page_no, clip) in CROPS.items():
    pix = doc[page_no].get_pixmap(clip=pymupdf.Rect(*clip), dpi=DPI)
    path = OUT % name
    pix.save(path)
    print(name, pix.width, "x", pix.height)
    tiles.append((name, path))

# emphasise Circle = 0.92 and fade the other dimensions of the vector
path = OUT % "center_vector"
im = Image.open(path).convert("RGBA")
w, h = im.size
y0, y1 = 0.355 * h, 0.545 * h
ov = Image.new("RGBA", im.size, (255, 255, 255, 0))
d = ImageDraw.Draw(ov)
d.rectangle((0, 0, w, y0), fill=(255, 255, 255, 120))
d.rectangle((0, y1, w, h), fill=(255, 255, 255, 120))
im = Image.alpha_composite(im, ov).convert("RGB")
d = ImageDraw.Draw(im)
d.rounded_rectangle((0.02 * w, y0, 0.985 * w, y1),
                    radius=int(0.05 * h), outline=(14, 111, 198), width=3)
im.save(path)

# verification montage
cols = 5
cell_w, cell_h = 260, 220
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (245, 245, 245))
d = ImageDraw.Draw(sheet)
for i, (name, path) in enumerate(tiles):
    t = Image.open(path)
    t.thumbnail((cell_w - 16, cell_h - 40))
    x = (i % cols) * cell_w + (cell_w - t.width) // 2
    y = (i // cols) * cell_h + 26
    sheet.paste(t, (x, y))
    d.text(((i % cols) * cell_w + 8, (i // cols) * cell_h + 6), name,
           fill=(20, 20, 20))
sheet.save("/tmp/opencode/overview_assets.png")
print("montage saved")
