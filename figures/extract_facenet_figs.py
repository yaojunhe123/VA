"""Crop FaceNet figures for the loss-design slide.

Source: Schroff, Kalenichenko, Philbin. "FaceNet: A Unified Embedding for
Face Recognition and Clustering." CVPR 2015.
arXiv: https://arxiv.org/pdf/1503.03832  (download to the path below first)

Outputs:
  - figures/facenet_fig3.pdf/.png       Fig. 3: triplet before/after geometry
  - figures/facenet_fig7_strip.pdf/.png Fig. 7: one row of a face cluster
"""

import pymupdf

SRC = "/tmp/opencode/facenet.pdf"     # arXiv:1503.03832
OUT = "/home/yaojunhe/VA/figures/%s"

CROPS = {
    # name: (page index, clip, dpi for the PNG preview)
    "facenet_fig3":        (2, (44.0, 168.0, 300.0, 229.0), 450),
    "facenet_fig7_strip":  (7, (319.0, 73.5, 534.5, 107.5), 450),
}

src = pymupdf.open(SRC)
for name, (page_no, box, dpi) in CROPS.items():
    clip = pymupdf.Rect(*box)
    out = pymupdf.open()
    page = out.new_page(width=clip.width, height=clip.height)
    page.show_pdf_page(page.rect, src, page_no, clip=clip)
    out.save(OUT % (name + ".pdf"))
    pix = src[page_no].get_pixmap(clip=clip, dpi=dpi)
    pix.save(OUT % (name + ".png"))
    print(name, pix.width, "x", pix.height)
