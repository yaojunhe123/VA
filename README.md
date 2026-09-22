# VA — VISAtlas Reproduction Talk

LaTeX (beamer) source of the VISAtlas reproduction presentation, built with the
custom **Lumen** beamer theme. All source is self-contained in this repository.

## Structure

```
.
├── talk.tex                        # presentation source (6 frames)
├── beamerthemelumen.sty            # Lumen theme (self-contained in repo root)
├── beamercolorthemelumen.sty
├── beamerfontthemelumen.sty
├── beamerinnerthemelumen.sty
├── beamerouterthemelumen.sty
├── figures/
│   ├── citation_provenance.py/.pdf # temporal citation provenance graph
│   ├── extract_overview_parts.py   # crops for the System Overview slide
│   ├── make_collection_thumbs.py   # thumbnails for the Data Collection slide
│   ├── center_*.png, left_*.png, right_*.png    # System Overview assets
│   ├── syn_*.png, rw_beagle*.png, rw_vis30k*.png # Data Collection assets
│   └── ...                         # earlier iterations kept for reference
├── data/
│   ├── citations.json              # 37 papers citing VISAtlas (Semantic Scholar)
│   └── references.json             # reference metadata query result
└── talk.pdf                        # built slides
```

## Build

Requires TeX Live with `lualatex`, Fira Sans / Fira Mono / FiraMath fonts.

```bash
lualatex -interaction=nonstopmode talk.tex
lualatex -interaction=nonstopmode talk.tex   # second run for page totals
```

## Asset generation

Sources used for the figure crops:

- VISAtlas paper PDF (Fig. 1 and Fig. 10) — System Overview and Data Collection.
- Released VISAtlas repository (`github.com/yilinye/VisAtlas-Code`):
  `Frontend/src/assets/static/{data2vis_imdb,imdb_Beagle,imdb_vis30k}` and
  `Backend/uploadImage` — representative collection and demo images.

Scripts in `figures/` regenerate the crops (paths point to the local copies of
the paper and repository).

## Deck outline

1. Title
2. Motivation — quotes from the VISAtlas paper + claim
3. Research questions
4. Related work — temporal citation provenance graph
5. VISAtlas System Overview — what goes in / what it does / what users can do
6. Data Collection — controlled coverage + realistic diversity
