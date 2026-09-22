"""Extract the running-example elements from VISAtlas Fig. 1.

Crops (from the Prediction block and the Visualization Gallery):
  input   -> the pie-chart image
  vector  -> the 11D interpretable prediction vector (Circle 0.92 highlighted,
             remaining dimensions faded)
  gallery -> three visually similar designs from the gallery
"""

import pymupdf
from PIL import Image, ImageDraw

SRC = "/mnt/c/Users/Administrator/Downloads/VISAtlas (1).pdf"
PAGE = 3
DPI = 500
OUT = "/home/yaojunhe/va-talk/figures/runexample_%s.png"

CROPS = {
    "input":   (424.2, 106.8, 443.6, 128.6),
    "vector":  (491.8, 106.9, 516.5, 129.4),
    "gallery": (417.8, 227.4, 500.1, 244.6),
}
# highlighted row in the vector crop (relative to crop height)
HILITE = (0.355, 0.545)

doc = pymupdf.open(SRC)
page = doc[PAGE]
for name, box in CROPS.items():
    pix = page.get_pixmap(clip=pymupdf.Rect(*box), dpi=DPI)
    pix.save(OUT % name)
    print(name, pix.width, "x", pix.height)

# fade the non-dominant dimensions, then highlight Circle = 0.92
path = OUT % "vector"
im = Image.open(path).convert("RGB")
w, h = im.size
overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
d = ImageDraw.Draw(overlay)
y0, y1 = HILITE[0] * h, HILITE[1] * h
d.rectangle((0, 0, w, y0), fill=(255, 255, 255, 165))
d.rectangle((0, y1, w, h), fill=(255, 255, 255, 165))
im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(im)
d.rounded_rectangle((0.02 * w, y0, 0.985 * w, y1),
                    radius=int(0.05 * h), outline=(14, 111, 198), width=3)
im.save(path)
print("vector faded + highlighted", im.size)
