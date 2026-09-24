"""Crop assets for the 'Image Embedding via CNN' slides (paper Fig. 2).

Sources (VISAtlas paper PDF, page 6 = index 5):
  - Fig. 2: input images -> ResNets (shared weights) -> embeddings -> triplet loss.

Outputs (repo-local):
  - embedding_fig2_full.pdf/.png  : full Fig. 2 (vector + preview)
  - embedding_fig2_trio.pdf/.png  : inputs + 3 ResNets + embeddings (no triplet box)
  - embedding_in_{n,m,l}.png      : the three input thumbnails
  - embedding_triplet.png         : the 'Triplet loss' box
"""

import pymupdf
from PIL import Image, ImageDraw

SRC = "/mnt/c/Users/Administrator/Downloads/VISAtlas (1).pdf"
PAGE = 5
OUT = "/home/yaojunhe/VA/figures/%s"
DPI = 500

VECTOR = {
    "embedding_fig2_full": (30.0, 42.0, 275.0, 170.0),
    "embedding_fig2_trio": (63.5, 44.5, 193.0, 158.5),
}

RASTER = {
    "embedding_in_n":    (64.0, 45.0, 98.0, 79.5),
    "embedding_in_m":    (64.0, 84.0, 98.0, 118.5),
    "embedding_in_l":    (64.0, 123.0, 98.0, 158.0),
    "embedding_triplet": (216.0, 89.0, 273.5, 112.5),
}

src = pymupdf.open(SRC)
tiles = []

for name, box in VECTOR.items():
    clip = pymupdf.Rect(*box)
    out = pymupdf.open()
    page = out.new_page(width=clip.width, height=clip.height)
    page.show_pdf_page(page.rect, src, PAGE, clip=clip)
    out.save(OUT % (name + ".pdf"))
    pix = src[PAGE].get_pixmap(clip=clip, dpi=350)
    pix.save(OUT % (name + ".png"))
    print(name, pix.width, "x", pix.height)
    tiles.append((name, OUT % (name + ".png")))

for name, box in RASTER.items():
    pix = src[PAGE].get_pixmap(clip=pymupdf.Rect(*box), dpi=DPI)
    path = OUT % (name + ".png")
    pix.save(path)
    print(name, pix.width, "x", pix.height)
    tiles.append((name, path))

cols = 3
cell_w, cell_h = 420, 340
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
sheet.save("/tmp/opencode/embedding_assets.png")
print("montage saved")
