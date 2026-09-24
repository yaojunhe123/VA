# VA — VISAtlas Reproduction Talk

LaTeX (beamer) source of the VISAtlas reproduction presentation, built with the
custom **Lumen** beamer theme. All source is self-contained in this repository.

## Structure

```
.
├── talk.tex                        # presentation source (7 sections, 25 frames)
├── beamerthemelumen.sty            # Lumen theme (self-contained in repo root)
├── beamercolorthemelumen.sty
├── beamerfontthemelumen.sty
├── beamerinnerthemelumen.sty
├── beamerouterthemelumen.sty
├── figures/
│   ├── citation_provenance.py/.pdf # temporal citation provenance graph
│   ├── extract_overview_parts.py   # crops for the System Overview slide
│   ├── extract_embedding_figs.py   # crops of Fig. 2 for the embedding slides
│   ├── extract_facenet_figs.py     # FaceNet Fig. 3 + Fig. 7 strip crops
│   ├── extract_interface_figs.py   # Ch.5 figures: Fig. 4d / Fig. 6 / Fig. 7
│   ├── extract_resnet_stages.py    # real ResNet50 activations (visatlas env)
│   ├── make_resnet_stages_fig.py   # activation panel: pixels -> maps -> 11-D
│   ├── make_collection_thumbs.py   # thumbnails for the Data Collection slide
│   ├── embedding_fig2_trio.pdf/.png, embedding_fig2_full.pdf/.png
│   │                               # Fig. 2: inputs -> ResNets -> embeddings
│   ├── embedding_in_{n,m,l}.png    # the three input thumbnails (anchor/same/different)
│   ├── facenet_fig3.pdf/.png       # anchor/positive/negative geometry (FaceNet)
│   ├── facenet_fig7_strip.pdf/.png # one cluster row: same identity, varied looks
│   ├── resnet_stages.png           # input -> conv1/conv3/conv5 -> GAP -> q
│   ├── fig6_pca/tsne/legend.png    # PCA vs. t-SNE alternatives (Fig. 6)
│   ├── fig4d.png                   # sampling + density radial overview
│   ├── fig7_interface.png          # interface: histogram/overview/query/gallery
│   ├── fig7_histogram.png          # Embedding Histogram panel (Fig. 7a)
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

- VISAtlas paper PDF — Fig. 1 (System Overview), Fig. 10 (real-world
  thumbnails), and Fig. 2 (Image Embedding via CNN: inputs, ResNets,
  embeddings, triplet loss).
- FaceNet paper PDF (Schroff et al., CVPR 2015, arXiv:1503.03832) — Fig. 3
  (triplet geometry) and Fig. 7 (face-cluster strip); `extract_facenet_figs.py`
  expects a local copy at `/tmp/opencode/facenet.pdf`.
- VISAtlas interface figures (Chapter 5 slides): `extract_interface_figs.py`
  crops Fig. 4(d), Fig. 6 (PCA/t-SNE/legend) and Fig. 7 from the paper PDF.
- Real ResNet50 activations for the embedding slide: run
  `extract_resnet_stages.py` inside the `visatlas` conda env (loads the
  released 11250.h5 + forvis2.h5 weights, uses `Crawled data/point/506.png`),
  then `make_resnet_stages_fig.py` with the system python.
- Released VISAtlas repository (`github.com/yilinye/VisAtlas-Code`):
  `Frontend/src/assets/static/{data2vis_imdb,imdb_Beagle,imdb_vis30k}` and
  `Backend/uploadImage` — representative collection and demo images.

Scripts in `figures/` regenerate the crops (paths point to the local copies of
the paper and repository).

## Deck outline

1. **Context** — Where, When, and by Whom
2. **Motivation & Research Questions** — paper quotes + claim; the four questions
3. **Related Work & Contributions** — citation provenance graph; contributions
4. **System & Method** — System Overview; Data Collection; Image Embedding via
   CNN (real ResNet50 activations); FaceNet triplet geometry -> VISAtlas
   objective; Why VISAtlas Avoids PCA and t-SNE (three-column comparison);
   How VISAtlas Builds an Interactive Embedding Space (central Fig. 4(d) hub)
5. **Evaluation: Case Studies** — Does real-world data help?; comparing
   collections; composites and retrieval; user study
6. **Our Reproduction & Discussion** — we ran the released system; documented
   weak spots; extreme 4-way composite; minimal-pair test; our critical take
7. **Impact & Conclusion** — from one paper to a research programme;
   take-home messages
