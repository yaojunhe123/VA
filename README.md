# VA — VISAtlas Reproduction Talk

LaTeX (beamer) source of the VISAtlas reproduction presentation, built with the
custom **Lumen** beamer theme. All source is self-contained in this repository.

## Structure

```
.
├── talk.tex                        # presentation source (8 frames)
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
│   ├── fig3_histogram.png          # full Embedding Histogram panel (Fig. 3b)
│   ├── fig3_point.png              # Point small multiple (zoom-in case)
│   ├── fig6_pca/tsne/legend.png    # PCA vs. t-SNE alternatives (Fig. 6)
│   ├── fig4a/b/c/d.png             # projection, overdrawing, density, sampling
│   ├── fig3_gallery.png            # Visualization Gallery panel (Fig. 3c)
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
  crops Fig. 3(b) (Embedding Histogram + Point small multiple) and 3(c)
  (Gallery), Fig. 4(a-d), Fig. 6 (PCA/t-SNE) and Fig. 7 from the paper PDF.
  The Fig. 3(b)/(c) crops have the paper's orange corner badges erased
  (`erase_corner_badge`); Fig. 7 has the paper's own a/b/c tag boxes masked
  (`MASK_BOXES` + gradient reconstruction) so only the slide's ①②③ remain.
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

1. Title
2. Motivation — quotes from the VISAtlas paper + claim
3. Research questions
4. Related work — temporal citation provenance graph
5. VISAtlas System Overview — what goes in / what it does / what users can do
6. Data Collection — controlled coverage + realistic diversity
7. Image Embedding via CNN — real ResNet50 activations: input image ->
   conv1/conv3/conv5 feature maps -> GAP -> 11-D probabilities
8. From Triplet Metric Learning to VISAtlas — FaceNet Fig. 3 (triplet
   geometry) + schematic embedding clusters vs. VISAtlas Fig. 2,
   L = L_CE + β·L_TR, type semantics and relative geometry
9. Why VISAtlas Avoids PCA and t-SNE — three-column comparison
   (PCA | t-SNE | VISAtlas): large Fig. 6 panels vs. Fig. 4(d) with light
   semantic-anchor arrows, closed by a one-line takeaway strip
10. How VISAtlas Builds an Interactive Embedding Space — central Fig. 4(d)
    Embedding Overview hub with four callouts: semantic projection, scalable
    rendering (overdrawing/density), linked Embedding Histogram, and
    query → similarity → gallery retrieval
11. Interactive Exploration and Visual Query — large Fig. 7 with only
    FILTER / QUERY / RETRIEVE callouts
