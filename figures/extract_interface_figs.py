"""Crop VISAtlas interface figures for the Chapter 5 (Visual Analytics) slides.

Sources (VISAtlas paper PDF):
  p7  Fig. 6 : PCA and t-SNE alternatives + color legend
  p7  Fig. 4d: sampling + density radial Embedding Overview
  p9  Fig. 7 : interface (histogram / overview / visual query / gallery)

Outputs into figures/:
  fig6_pca.png, fig6_tsne.png, fig6_legend.png
  fig4d.png
  fig7_interface.png, fig7_histogram.png
"""

import pymupdf

SRC = "/mnt/c/Users/Administrator/Downloads/VISAtlas (1).pdf"
OUT = "/home/yaojunhe/VA/figures/%s.png"

CROPS = {
    "fig6_pca":       (7, (293.0, 46.0, 391.0, 138.0)),
    "fig6_tsne":      (7, (401.0, 46.0, 483.0, 138.0)),
    "fig6_legend":    (7, (490.0, 46.0, 539.0, 138.0)),
    "fig4d":          (6, (422.0, 46.0, 537.0, 157.0)),
    "fig7_interface": (8, (26.0, 43.0, 278.0, 292.0)),
    "fig7_histogram": (8, (33.0, 47.0, 146.0, 160.0)),
}

doc = pymupdf.open(SRC)
for name, (page_no, box) in CROPS.items():
    pix = doc[page_no].get_pixmap(clip=pymupdf.Rect(*box), dpi=420)
    pix.save(OUT % name)
    print(name, pix.width, "x", pix.height)
