"""Temporal citation provenance graph for VISAtlas (v3).

Left: intellectual foundations (papers cited by VISAtlas).
Centre: VISAtlas spine (online 2022, TVCG vol. 30, 2024).
Right: subsequent influence (papers citing VISAtlas).
Horizontal = time, vertical lanes = research themes, colours = themes,
thick faint trunks = thematic knowledge streams, thin edges = citations.
"""

from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.textpath import TextPath
import matplotlib.patheffects as pe

HALO = [pe.withStroke(linewidth=1.6, foreground="white")]

FIRA = "/home/yaojunhe/.fonts/fira"
for face in ("Regular", "Bold", "Italic", "Medium", "SemiBold"):
    fm.fontManager.addfont(f"{FIRA}/FiraSans-{face}.otf")

FP_REG = fm.FontProperties(fname=f"{FIRA}/FiraSans-Regular.otf")
FP_SEMI = fm.FontProperties(fname=f"{FIRA}/FiraSans-SemiBold.otf")

plt.rcParams.update({
    "font.family": "Fira Sans",
    "font.size": 6,
    "pdf.fonttype": 42,
    "axes.linewidth": 0,
})

COLORS = {
    "collections": "#1B4F8A",
    "retrieval":   "#0E6FC6",
    "embedding":   "#2A9D8F",
    "apps":        "#5B6B7C",
}
LANE_NAMES = {
    "collections": ("Collections &", "Datasets"),
    "retrieval":   ("Retrieval &", "Exploration"),
    "embedding":   ("Embedding &", "ML"),
    "apps":        ("Applications &", "Systems"),
}
LANE_ORDER = ["collections", "retrieval", "embedding", "apps"]

# (theme, year, author, short title, representative)
CITED = [
    ("collections", 2011, "Savva",   "ReVision",  False),
    ("collections", 2018, "Battle",  "Beagle",    True),
    ("collections", 2018, "Luo",     "DeepEye",   False),
    ("collections", 2019, "Dibia",   "Data2Vis",  False),
    ("collections", 2021, "Chen",    "VIS30K",    True),
    ("collections", 2022, "Deng",    "VisImages", False),
    ("retrieval",   2017, "Jung",    "ChartSense", False),
    ("retrieval",   2020, "Ma",      "ScatterNet", False),
    ("retrieval",   2021, "Zeng",    "VIStory",   False),
    ("retrieval",   2021, "Luo",     "ChartOCR",  True),
    ("retrieval",   2022, "Zhao",    "ChartSeer", True),
    ("retrieval",   2022, "Li",      "StructRetr", False),
    ("embedding",   1992, "Boser",   "SVM",       False),
    ("embedding",   1997, "Hoffman", "RadViz",    False),
    ("embedding",   2008, "Maaten",  "t-SNE",     True),
    ("embedding",   2015, "Cheng",   "CtxLayout", False),
    ("embedding",   2016, "He",      "ResNet",    True),
    ("embedding",   2018, "McInnes", "UMAP",      True),
]
CITING = [
    ("retrieval",   2022, "Ying",     "VAID",          True),
    ("retrieval",   2023, "Xiao",     "WYTIWYR",       False),
    ("retrieval",   2024, "Arnold",   "HeritageSearch", True),
    ("retrieval",   2024, "Nowak",    "ChartRetrieval", False),
    ("retrieval",   2025, "Nguyen",   "Safire",        False),
    ("retrieval",   2026, "Nguyen",   "DataLiteracy",  False),
    ("collections", 2023, "Zhang",    "OldVisOnline",  True),
    ("collections", 2023, "Ye",       "Picasso",       False),
    ("collections", 2024, "Tu",       "KG-PRE-view",   True),
    ("collections", 2024, "Chen",     "ImageTypology", False),
    ("collections", 2025, "Wang",     "LLMCollections", False),
    ("embedding",   2023, "Jung",     "ProjEnsemble",  False),
    ("embedding",   2023, "Huang",    "VA+EmbSTAR",    False),
    ("embedding",   2024, "Zhou",     "ChartKG",       True),
    ("embedding",   2024, "Ye",       "ModalChorus",   True),
    ("embedding",   2025, "Czerw.",   "E-comm.Emb.",   False),
    ("embedding",   2025, "Ye",       "AIPaintings",   False),
    ("embedding",   2026, "Lawonn",   "WatchesLatent", False),
    ("embedding",   2026, "Yu",       "ParallelClust.", False),
    ("embedding",   2026, "Ye",       "DKMap",         True),
    ("apps",        2023, "Li",       "Storytelling",  False),
    ("apps",        2024, "Hao",      "FinFlier",      True),
    ("apps",        2024, "Grotsch.", "AEye",          False),
    ("apps",        2024, "Xia",      "RE-IDVIS",      False),
    ("apps",        2025, "Bauer",    "QVis",          True),
    ("apps",        2026, "Bujack",   "AutomaticVis.", False),
]
# aggregated minor citing papers: (theme, year, count)
AGG = [
    ("embedding", 2024, 4),
    ("apps",      2023, 2),
    ("apps",      2025, 5),
]

# ---------------------------------------------------------------- geometry
W, H = 14.7, 6.6
HEADER_Y = 6.45
LANE_TOP, LANE_BOTTOM_LIMIT = 6.15, 1.00
SPINE_X0, SPINE_X1 = 6.85, 7.85
LEFT_ELBOW_Y, LEFT_ELBOW_X, LEFT_X1 = 2013, 3.00, 5.80
RIGHT_X0, RIGHT_STEP = 8.35, 1.25
OFFSET = 0.24
LANE_PAD, LANE_GAP = 0.03, 0.08
REP_L1, REP_L2, SEC_SIZE, AGG_SIZE = 4.2, 3.8, 3.9, 3.9


def year_to_x_left(year):
    if year <= LEFT_ELBOW_Y:
        return 1.75 + (year - 1992) * (LEFT_ELBOW_X - 1.75) / (
            LEFT_ELBOW_Y - 1992)
    return LEFT_ELBOW_X + (year - LEFT_ELBOW_Y) * (LEFT_X1 - LEFT_ELBOW_X) / (
        2022 - LEFT_ELBOW_Y)


def year_to_x_right(year):
    return RIGHT_X0 + (year - 2022) * RIGHT_STEP


def text_width(s, size, bold=False):
    tp = TextPath((0, 0), s, size=size, prop=FP_SEMI if bold else FP_REG)
    return tp.get_extents().width * 2.54 / 72.0


def node_label(node):
    _, year, author, short, rep = node
    return f"{author} '{str(year)[2:]}", short if rep else None


def build_items(nodes, xfun, offset_same_year=False):
    if offset_same_year:
        groups = defaultdict(list)
        for node in nodes:
            groups[node[1]].append(node)
        idx = {}
        for year, group in groups.items():
            for k, node in enumerate(group):
                idx[id(node)] = k
    items = []
    for node in nodes:
        x = xfun(node[1])
        if offset_same_year and len(groups[node[1]]) > 1:
            x += OFFSET * idx[id(node)]
        l1, l2 = node_label(node)
        w = max(text_width(l1, REP_L1 if node[4] else SEC_SIZE, node[4]),
                text_width(l2, REP_L2) if l2 else 0.0)
        iid = ("node", node)
        items.append((iid, x, x - 0.02, x + 0.09 + w))
    return items


def build_agg_items(aggs, xfun):
    items = []
    for theme, year, count in aggs:
        x = xfun(year)
        label = f"+{count} other works"
        w = text_width(label, AGG_SIZE)
        items.append((("agg", (theme, year, count)), x, x - 0.02,
                      x + 0.09 + w))
    return items


def pack_rows(items):
    rows = []
    out = []
    for iid, x, s0, s1 in sorted(items, key=lambda t: t[2]):
        for ri, row in enumerate(rows):
            if all(s1 + 0.05 < a or s0 > b + 0.05 for a, b in row):
                row.append((s0, s1))
                out.append((iid, x, ri))
                break
        else:
            rows.append([(s0, s1)])
            out.append((iid, x, len(rows) - 1))
    return out


def draw_node(ax, iid, x, y, theme):
    if iid[0] == "node":
        node = iid[1]
        _, year, author, short, rep = node
        l1 = f"{author} '{str(year)[2:]}"
        if rep:
            ax.scatter([x], [y], s=17, color=COLORS[theme], zorder=4,
                       edgecolor="white", linewidth=0.4)
            ax.text(x + 0.09, y + 0.062, l1, fontsize=REP_L1,
                    fontweight="bold", color="#1B2430", ha="left",
                    va="center", zorder=5, path_effects=HALO)
            ax.text(x + 0.09, y - 0.075, short, fontsize=REP_L2,
                    color=COLORS[theme], ha="left", va="center", zorder=5,
                    path_effects=HALO)
        else:
            ax.scatter([x], [y], s=9, color=COLORS[theme], alpha=0.85,
                       zorder=4, edgecolor="white", linewidth=0.3)
            ax.text(x + 0.09, y, l1, fontsize=SEC_SIZE, color="#3A4A5A",
                    ha="left", va="center", zorder=5, path_effects=HALO)
    else:
        _, year, count = iid[1]
        ax.scatter([x], [y], s=11, facecolor="white",
                   edgecolor=COLORS[theme], linewidth=0.6, zorder=4)
        ax.text(x + 0.09, y, f"+{count} other works", fontsize=AGG_SIZE,
                color="#5B6B7C", ha="left", va="center", zorder=5,
                path_effects=HALO)


def main():
    fig = plt.figure(figsize=(W / 2.54, H / 2.54))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---- pack ---------------------------------------------------------
    packed = {"left": {}, "right": {}}
    lane_rows = {}
    for lane in LANE_ORDER:
        packed["left"][lane] = pack_rows(build_items(
            [n for n in CITED if n[0] == lane], year_to_x_left,
            offset_same_year=True))
        right_nodes = [n for n in CITING if n[0] == lane]
        right_aggs = [a for a in AGG if a[0] == lane]
        packed["right"][lane] = pack_rows(
            build_items(right_nodes, year_to_x_right)
            + build_agg_items(right_aggs, year_to_x_right))
        lane_rows[lane] = max(
            [item[2] + 1 for item in packed["left"][lane]]
            + [item[2] + 1 for item in packed["right"][lane]] + [1])

    avail = LANE_TOP - LANE_BOTTOM_LIMIT
    total_rows = sum(lane_rows.values())
    pitch = (avail - (4 * 2 * LANE_PAD + 3 * LANE_GAP)) / total_rows

    lane_y = {}
    y = LANE_TOP
    for lane in LANE_ORDER:
        h = 2 * LANE_PAD + lane_rows[lane] * pitch
        lane_y[lane] = (y, y - h)
        y -= h + LANE_GAP
    lane_bottom = y + LANE_GAP

    # ---- narrative headers -------------------------------------------
    ax.text(1.75, HEADER_Y, "INTELLECTUAL FOUNDATIONS", fontsize=4.6,
            fontweight="bold", color="#5B6B7C", ha="left", va="center",
            zorder=5)
    ax.text(W / 2, HEADER_Y, "VISATLAS", fontsize=6.0, fontweight="bold",
            color="#1B4F8A", ha="center", va="center", zorder=5)
    ax.text(W - 0.10, HEADER_Y, "SUBSEQUENT INFLUENCE", fontsize=4.6,
            fontweight="bold", color="#5B6B7C", ha="right", va="center",
            zorder=5)

    # ---- central spine -----------------------------------------------
    ax.add_patch(FancyBboxPatch(
        (SPINE_X0, lane_bottom), SPINE_X1 - SPINE_X0, LANE_TOP - lane_bottom,
        boxstyle="round,pad=0.0,rounding_size=0.12",
        facecolor="#1B4F8A", edgecolor="none", zorder=3))
    sx = (SPINE_X0 + SPINE_X1) / 2
    sy = (LANE_TOP + lane_bottom) / 2
    ax.text(sx - 0.17, sy, "VISAtlas", fontsize=8.5, fontweight="bold",
            color="white", ha="center", va="center", rotation=90, zorder=4)
    ax.text(sx + 0.13, sy, "Ye · Huang · Zeng", fontsize=3.4, color="#C6D8EA",
            ha="center", va="center", rotation=90, zorder=4)
    ax.text(sx + 0.31, sy, "Online 2022 · TVCG Vol. 30 (2024)", fontsize=3.4,
            color="#C6D8EA", ha="center", va="center", rotation=90, zorder=4)

    # ---- lanes: trunks, nodes, citation edges ------------------------
    for lane in LANE_ORDER:
        y0, y1 = lane_y[lane]
        yc = (y0 + y1) / 2
        ax.plot([0.06, W - 0.06], [y1, y1], color="#E8EEF5", lw=0.5,
                zorder=0.2)
        left_items = packed["left"][lane]
        right_items = packed["right"][lane]

        # thematic trunks
        if left_items:
            x_start = min(x for _, x, _ in left_items) - 0.10
            ax.add_patch(FancyArrowPatch(
                (x_start, yc), (SPINE_X0 - 0.02, yc),
                arrowstyle="-|>", mutation_scale=6, lw=2.2,
                color=COLORS[lane], alpha=0.16, zorder=0.8))
        if right_items:
            x_end = max(x for _, x, _ in right_items) + 0.10
            ax.add_patch(FancyArrowPatch(
                (SPINE_X1 + 0.02, yc), (x_end, yc),
                arrowstyle="-|>", mutation_scale=6, lw=2.2,
                color=COLORS[lane], alpha=0.16, zorder=0.8))

        for side in ("left", "right"):
            for iid, x, ri in packed[side][lane]:
                y_node = y0 - LANE_PAD - (ri + 0.5) * pitch
                is_rep = iid[0] == "node" and iid[1][4]
                lw, alpha = (0.6, 0.5) if is_rep else (0.45, 0.32)
                if side == "left":
                    p0 = (x + 0.04, y_node)
                    p1 = (x + 0.32, yc)
                else:
                    p0 = (x - 0.32, yc)
                    p1 = (x - 0.04, y_node)
                rad = 0.18 if y_node >= yc else -0.18
                ax.add_patch(FancyArrowPatch(
                    p0, p1, connectionstyle=f"arc3,rad={rad}",
                    arrowstyle="-|>", mutation_scale=3.4, lw=lw,
                    color=COLORS[lane], alpha=alpha, zorder=1.2))
                draw_node(ax, iid, x, y_node, lane)

        # lane labels and counts
        n_cited = sum(1 for n in CITED if n[0] == lane)
        n_citing = (sum(1 for n in CITING if n[0] == lane)
                    + sum(a[2] for a in AGG if a[0] == lane))
        nm1, nm2 = LANE_NAMES[lane]
        ax.text(0.10, yc + 0.115, nm1, fontsize=5.2, fontweight="bold",
                color=COLORS[lane], ha="left", va="center", zorder=5)
        ax.text(0.10, yc - 0.015, nm2, fontsize=5.2, fontweight="bold",
                color=COLORS[lane], ha="left", va="center", zorder=5)
        ax.text(0.10, yc - 0.155, f"{n_cited} cited", fontsize=4.0,
                color="#5B6B7C", ha="left", va="center", zorder=5)
        if n_citing:
            ax.text(W - 0.10, yc, f"{n_citing} citing", fontsize=4.0,
                    color="#5B6B7C", ha="right", va="center", zorder=5)

    # ---- time axes ----------------------------------------------------
    for x0, x1 in ((1.75, LEFT_X1), (RIGHT_X0 - 0.10, RIGHT_X0 + 4 * RIGHT_STEP + 0.10)):
        ax.plot([x0, x1], [0.80, 0.80], color="#C6D8EA", lw=0.6, zorder=0.5)
    for yr in (1992, 2000, 2010, 2015, 2020, 2022):
        x = year_to_x_left(yr)
        ax.plot([x, x], [0.80, 0.74], color="#C6D8EA", lw=0.6, zorder=0.5)
        ax.text(x, 0.63, str(yr), fontsize=3.8, color="#5B6B7C",
                ha="center", va="top", zorder=5)
    ax.plot([LEFT_ELBOW_X, LEFT_ELBOW_X], [lane_bottom, 0.80],
            color="#C6D8EA", lw=0.5, ls=(0, (2.2, 2.2)), zorder=0.5)
    for yr in range(2022, 2027):
        x = year_to_x_right(yr)
        ax.plot([x, x], [0.80, 0.74], color="#C6D8EA", lw=0.6, zorder=0.5)
        ax.text(x, 0.63, str(yr), fontsize=3.8, color="#5B6B7C",
                ha="center", va="top", zorder=5)

    # ---- captions -----------------------------------------------------
    ax.text(3.70, 0.42, "18 representative references · 1992–2022",
            fontsize=4.0, color="#5B6B7C", ha="center", va="center")
    ax.text(11.20, 0.42, "all 37 citing papers · 2022–2026",
            fontsize=4.0, color="#5B6B7C", ha="center", va="center")
    ax.text(W / 2, 0.17,
            "Where did VISAtlas come from intellectually?   ·   "
            "Which research themes contributed to it?   ·   "
            "Where did its influence propagate afterward?",
            fontsize=4.6, color="#1B2430", ha="center", va="center")

    fig.savefig("/home/yaojunhe/va-talk/figures/citation_provenance.pdf")
    fig.savefig("/home/yaojunhe/va-talk/figures/citation_provenance.png",
                dpi=340)
    print("saved; lane rows:", lane_rows, "pitch %.3f" % pitch)


if __name__ == "__main__":
    main()
