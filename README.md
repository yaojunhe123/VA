# VA — VISAtlas Reproduction Talk

LaTeX (beamer) source of the VISAtlas reproduction presentation, built with the
custom **Lumen** beamer theme. All source is self-contained in this repository.

## Structure

```
.
├── talk.tex                        # presentation source (4 frames)
├── beamerthemelumen.sty            # Lumen theme (self-contained in repo root)
├── beamercolorthemelumen.sty
├── beamerfontthemelumen.sty
├── beamerinnerthemelumen.sty
├── beamerouterthemelumen.sty
├── figures/
│   ├── citation_provenance.py      # generator for the citation provenance figure
│   └── citation_provenance.pdf     # vector figure included by talk.tex
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

## Citation provenance figure

`figures/citation_provenance.py` regenerates the temporal citation provenance
graph (time axis × four thematic lanes, backward citations on the left, forward
citations on the right, VISAtlas spine in the centre):

```bash
python3 figures/citation_provenance.py
```

It needs `matplotlib` and the Fira Sans fonts (see `FIRA` path in the script).

## Deck outline

1. Title
2. Motivation — quotes from the VISAtlas paper + claim
3. Research questions
4. Related work — temporal citation provenance graph
