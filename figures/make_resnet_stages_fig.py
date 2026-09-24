"""Compose the ResNet50 activation figure for the embedding slide.

Reads /tmp/opencode/act/*.npy (produced by extract_resnet_stages.py) and
writes figures/resnet_stages.png: input image -> early/middle/deep feature
maps (3 representative channels each) -> GAP vector -> 11-D probabilities.

Run with the system python (matplotlib):
    /usr/bin/python3 figures/make_resnet_stages_fig.py
"""

import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

ACT = "/tmp/opencode/act"
OUT = "/home/yaojunhe/VA/figures/resnet_stages.png"

PRIMARY = "#1B4F8A"
EDGE = "#C6D8EA"
SLATE = "#5B6B7C"

FIRA = "/home/yaojunhe/.fonts/fira"
for face in ("Regular", "Bold", "Medium", "SemiBold"):
    fm.fontManager.addfont(f"{FIRA}/FiraSans-{face}.otf")
plt.rcParams.update({"font.family": "Fira Sans"})

CMAP = LinearSegmentedColormap.from_list(
    "lumen", ["#FFFFFF", "#DCE8F4", "#8FB4D8", "#3E74A8", "#1B4F8A"])

inp = np.load(f"{ACT}/input.npy")
conv1 = np.load(f"{ACT}/conv1.npy")
mid = np.load(f"{ACT}/mid.npy")
deep = np.load(f"{ACT}/deep.npy")
gap = np.load(f"{ACT}/gap.npy")
probs = np.load(f"{ACT}/probs.npy")


def norm(a):
    a = a.astype(np.float32)
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    return np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1)


W, H = 6.4, 1.6
fig = plt.figure(figsize=(W, H), dpi=300)


def add_ax(x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


def show(ax, arr):
    ax.imshow(arr, cmap=CMAP, interpolation="nearest", aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(EDGE)
        s.set_linewidth(0.5)


# ---- panels ----
ax = add_ax(0.05, 0.27, 1.60, 0.80)
ax.imshow(inp, aspect="equal")
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(EDGE)
    s.set_linewidth(0.5)

for arr, x in [(conv1, 1.95), (mid, 2.85), (deep, 3.75)]:
    for ch, y in zip(arr, (0.84, 0.50, 0.16)):
        show(add_ax(x, y, 0.70, 0.34), ch)

show(add_ax(4.62, 0.16, 0.22, 1.02), norm(gap)[:, None])

ax = add_ax(5.06, 0.16, 1.28, 1.02)
ax.bar(range(11), probs, color=[PRIMARY if i == int(np.argmax(probs)) else EDGE
                                for i in range(11)], width=0.8)
ax.set_xlim(-0.6, 10.6)
ax.set_ylim(0, 1.0)
ax.axis("off")
ax.axhline(0, color=SLATE, linewidth=0.5)

# ---- arrows ----
for x0, x1 in [(1.67, 1.93), (2.67, 2.83), (3.57, 3.73), (4.47, 4.60), (4.86, 5.04)]:
    fig.add_artist(FancyArrowPatch(
        (x0 / W, 0.67 / H), (x1 / W, 0.67 / H),
        transform=fig.transFigure, color=PRIMARY, linewidth=0.9,
        arrowstyle="-|>", mutation_scale=5))

# ---- labels ----
labels = [
    (0.85, "input", None),
    (2.30, "early features", None),
    (3.20, "mid-level features", None),
    (4.10, "deep features", None),
    (4.73, "GAP", "2048-D"),
    (5.70, "11-D output", "distribution"),
]
for cx, line1, line2 in labels:
    fig.text(cx / W, 1.36 / H, line1, ha="center", va="bottom",
             fontsize=5.4, color="#1B2430")
    if line2:
        fig.text(cx / W, 1.20 / H, line2, ha="center", va="bottom",
                 fontsize=4.4, color=SLATE, style="italic")

fig.savefig(OUT, dpi=300, facecolor="white")
print("saved", OUT)
