"""Crop VISAtlas interface figures for the Chapter 5 (Visual Analytics) slides.

Sources (VISAtlas paper PDF):
  p6  Fig. 3b: Embedding Histogram panel + Point small multiple
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
    "fig3_histogram": (5, (335.0, 470.5, 533.0, 587.5)),
    "fig3_point":     (5, (337.0, 550.0, 382.0, 584.0)),
    "fig6_pca":       (7, (292.0, 46.5, 390.5, 138.5)),
    "fig6_tsne":      (7, (400.5, 46.5, 497.5, 138.5)),
    "fig6_legend":    (7, (500.0, 46.5, 539.0, 138.5)),
    "fig4a":          (6, (90.0, 48.5, 181.0, 145.0)),
    "fig4b":          (6, (191.0, 49.0, 294.0, 145.0)),
    "fig4c":          (6, (304.0, 49.0, 399.0, 145.0)),
    "fig4d":          (6, (430.0, 52.2, 525.0, 143.8)),
    "fig3_gallery":   (5, (335.0, 590.0, 533.0, 709.0)),
    "fig7_interface": (8, (26.0, 43.0, 278.0, 292.0)),
    "fig7_histogram": (8, (33.0, 47.0, 146.0, 160.0)),
}

# Crops that still contain the paper's own orange corner badge ("b" / "c");
# erase it by row-copying the surrounding background.
ERASE_BADGE = ("fig3_histogram", "fig3_gallery")

# Fig. 7: the paper's own a/b/c tag boxes would duplicate the slide's ①②③
# numbering; mask them with white (pixel boxes measured on the crop).
MASK_BOXES = {
    "fig7_interface": [
        (104, 612, 660, 691),      # a  Filtering by attributes
        (818, 612, 1326, 691),     # b  Filtering by points
        (811, 996, 1134, 1073, 241),  # c  Visual query (left part, bg gray)
    ],
}

# Right part of the c box overlapped the query panel edge; rebuild that strip
# by tiling the clean panel edge from just below the box.
RECONSTRUCT = {
    "fig7_interface": [
        (1135, 1200, 996, 1074),
    ],
}


def erase_corner_badge(path, pad=10):
    """Erase the paper's orange corner badge: restore the teal title bar and
    leave the rest white (no streaks)."""
    from collections import Counter

    import numpy as np
    from PIL import Image
    from scipy import ndimage

    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    h, w, _ = a.shape
    search = a[: int(h * 0.35), : int(w * 0.25)].astype(int)
    r, g, b = search[..., 0], search[..., 1], search[..., 2]
    mask = ((r > 200) & (g > 70) & (g < 190) & (b < 110)).astype(np.uint8)
    lab, _n = ndimage.label(mask)
    corner_ids = [lab[y, x] for y in range(0, min(120, h), 10)
                  for x in range(0, min(120, w), 10) if lab[y, x] > 0]
    cid = Counter(corner_ids).most_common(1)[0][0]
    ys, xs = np.where(lab == cid)
    y0, y1, x1 = int(ys.min()), int(ys.max()), int(xs.max())

    fill_to = min(x1 + pad, w - 1)
    clean_cols = [c for c in (110, 120, 130, 140, 150) if c < w]

    def is_teal(c):
        return (c[1] > 150 and c[2] > 150 and (int(c[1]) - int(c[0])) > 18
                and abs(int(c[1]) - int(c[2])) < 16)

    def row_is_teal(y):
        return sum(1 for x in clean_cols if is_teal(a[y, x])) >= 3

    teal_rows = [y for y in range(h) if row_is_teal(y)]
    samples = np.array([[a[y, x] for y in teal_rows] for x in clean_cols])
    teal = np.median(samples.reshape(-1, 3).astype(np.float32), axis=0).astype(np.uint8)

    out = a.copy()
    for y in range(0, min(h, y1 + pad + 4)):
        out[y, : fill_to + 1] = teal if row_is_teal(y) else (255, 255, 255)
    Image.fromarray(out).save(path)
    print("  erased badge", path.split("/")[-1],
          f"(x1={x1}, y={y0}..{y1}, filled {fill_to}px wide)")


doc = pymupdf.open(SRC)
for name, (page_no, box) in CROPS.items():
    pix = doc[page_no].get_pixmap(clip=pymupdf.Rect(*box), dpi=420)
    pix.save(OUT % name)
    print(name, pix.width, "x", pix.height)
    if name in ERASE_BADGE:
        erase_corner_badge(OUT % name)
    if name in MASK_BOXES or name in RECONSTRUCT:
        import numpy as np
        from PIL import Image as _Image
        _im = _Image.open(OUT % name).convert("RGB")
        _a = np.asarray(_im).copy()
        for box in MASK_BOXES.get(name, []):
            x0, y0, x1, y1 = box[:4]
            fill = box[4] if len(box) > 4 else 255
            _a[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = fill
        for (x0, x1, y0, y1) in RECONSTRUCT.get(name, []):
            for xx in range(x0, x1):
                top = np.median(_a[max(0, y0 - 4):y0, xx].astype(np.float32), axis=0)
                bot = np.median(_a[y1 + 1:y1 + 5, xx].astype(np.float32), axis=0)
                t = np.linspace(0.0, 1.0, y1 - y0)[:, None]
                _a[y0:y1, xx] = (top[None, :] * (1 - t) + bot[None, :] * t).astype(np.uint8)
        _Image.fromarray(_a).save(OUT % name)
        print("  masked tag boxes", name)
