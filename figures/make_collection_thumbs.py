"""Prepare representative collection thumbnails for the Data Collection slide.

Sources (released VISAtlas repository, local copy):
  Frontend/src/assets/static/data2vis_imdb  -> synthetic collection (Data2Vis)
  Frontend/src/assets/static/imdb_Beagle    -> web-crawled collection
  Frontend/src/assets/static/imdb_vis30k    -> IEEE VIS publication collection
  Backend/uploadImage                       -> demo/query images
"""

import os
from PIL import Image

REPO = "/home/yaojunhe/repro/VisAtlas-Code"
OUT = "/home/yaojunhe/va-talk/figures/%s.png"
CANVAS = (480, 360)

PICKS = {
    # synthetic side
    "syn_d2v_bar":   (f"{REPO}/Frontend/src/assets/static/data2vis_imdb/17.png", 0),
    "syn_d2v_line":  (f"{REPO}/Frontend/src/assets/static/data2vis_imdb/88.png", 0),
    "syn_d2v_scat":  (f"{REPO}/Frontend/src/assets/static/data2vis_imdb/3000.png", 0),
    "syn_demo_area": (f"{REPO}/Backend/uploadImage/area.png", 0),
    "syn_demo_donut": (f"{REPO}/Backend/uploadImage/donut-chart-1.png", 0),
    "syn_demo_hist": (f"{REPO}/Backend/uploadImage/histogram.jpg", 0),
    # real-world side
    "rw_beagle1": (f"{REPO}/Frontend/src/assets/static/imdb_Beagle/42.png", 0),
    "rw_beagle2": (f"{REPO}/Frontend/src/assets/static/imdb_Beagle/777.png", 0),
    "rw_beagle3": (f"{REPO}/Frontend/src/assets/static/imdb_Beagle/3000.png", 0),
    "rw_vis30k1": (f"{REPO}/Frontend/src/assets/static/imdb_vis30k/17.png", 0),
    "rw_vis30k2": (f"{REPO}/Frontend/src/assets/static/imdb_vis30k/42.png", 0),
    "rw_vis30k3": (f"{REPO}/Frontend/src/assets/static/imdb_vis30k/3000.png", 0),
}


def trim_white(im, thr=246):
    gray = im.convert("L").point(lambda v: 255 if v < thr else 0)
    bbox = gray.getbbox()
    if bbox:
        pad = 4
        bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
        im = im.crop(bbox)
    return im


def fit_on_canvas(path):
    im = trim_white(Image.open(path).convert("RGB"))
    maxw, maxh = CANVAS[0] - 10, CANVAS[1] - 10
    scale = min(maxw / im.width, maxh / im.height)
    im = im.resize((max(1, int(im.width * scale)),
                    max(1, int(im.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGB", CANVAS, (255, 255, 255))
    canvas.paste(im, ((CANVAS[0] - im.width) // 2,
                      (CANVAS[1] - im.height) // 2))
    return canvas


for name, (path, _) in PICKS.items():
    canvas = fit_on_canvas(path)
    canvas.save(OUT % name)
    print(name, "<-", os.path.basename(path))
