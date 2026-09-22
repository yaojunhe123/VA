"""Extract Fig. 1 (system overview) from the VISAtlas paper PDF.

Crops the figure region (without the figure caption) and writes
figures/visatlas-overview.pdf (vector) plus a PNG preview.
"""

import pymupdf

SRC = "/mnt/c/Users/Administrator/Downloads/VISAtlas (1).pdf"
PAGE = 3                      # 0-based: page 4 of the paper
CLIP = (301.0, 43.0, 536.0, 260.0)
OUT = "/home/yaojunhe/va-talk/figures/visatlas-overview"

src = pymupdf.open(SRC)
clip = pymupdf.Rect(*CLIP)

out = pymupdf.open()
page = out.new_page(width=clip.width, height=clip.height)
page.show_pdf_page(page.rect, src, PAGE, clip=clip)
out.save(OUT + ".pdf")

pix = src[PAGE].get_pixmap(clip=clip, dpi=350)
pix.save(OUT + ".png")
print("saved", OUT + ".pdf/.png", pix.width, "x", pix.height)
