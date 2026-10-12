# Alessio Olivieri — portfolio

A lightweight static GitHub Pages site. No frontend framework, JavaScript bundle or build step is required.

## Pages

- `index.html`: introduction, three recent project previews, biography and contact.
- `projects.html`: curated project index, personal work separated from public collaborations, and a collapsible selection of smaller projects.
- `projects/*.html`: five case studies with results, contribution, experimental context, figures and source links.
- `cv.pdf` / `cv.tex`: the existing résumé and its LaTeX source. All “View CV” links open the PDF directly.

Serve locally with `python3 -m http.server 8000`. GitHub Pages serves the files in the repository. The existing CV workflow only runs when its LaTeX source or workflow changes.

## Editing

Edit the HTML directly. Shared styles are in `assets/site.css` (the original design) and `assets/showcase.css` (project pages, figures and responsive layouts). Preserve dates and contribution scope when updating a result. The project index is newest first within each group. The homepage features three recent projects; GitHub remains the complete repository index.

Figures link to their full-size assets. Native HTML disclosures expose exact benchmark values and additional projects without requiring JavaScript. Images have intrinsic dimensions and descriptive alternatives; reduced-motion and visible keyboard-focus styles are included.

## Figures and evidence

`assets/projects/data/benchmarks.json` stores the exact numerical values, source URLs and evaluation context used by the custom charts. To regenerate the three SVG charts, install matplotlib and run:

```sh
python3 tools/render_figures.py
```

- **ViT:** `vit-timing.svg` is replotted from the committed Ryzen 7 4700U benchmark. It shows average evaluation-workload time over ten runs, before retraining, not per-image latency. `vit-circuit.webp` and `vit-dataset.webp` are extracted from Alessio's *Mechanistic Interpretability for Vision Models Optimization* presentation, 19 June 2025, slides 11 and 8 respectively. The 55.24% retrained validation result is separate from the timing sweep. Dataset sample imagery originates from the Tiny ImageNet experiment.
- **Swing:** `swing-instruction-dag.webp` and `swing-original-benchmark.webp` are extracted from Alessio's *Implementation of Swing algorithm on NCCL* thesis presentation, 16 December 2024, slides 25 and 35. The first figure illustrates the visualizer using an AllReduce ring, not Swing. The benchmark is preserved as an original image because raw values were not supplied. It shows a prototype limitation, not a demonstrated speedup.
- **Traffic:** `traffic-ablation.svg` uses the published `TFE-GNN/public-release` result table. Error bars show sample SD across three training seeds on one fixed split, not confidence intervals. Architecture attribution remains with Zhang et al., WWW 2023; the case study describes an adaptation and independent experiments.
- **Surgical workflow:** `surgical-comparison.svg` uses the team's final benchmark. Frame accuracy and segmental F1 have different winning model/feature configurations. The page identifies the four-person team and Alessio's contribution without attributing all implementations to him.
- **Gear S3:** `gear-integration.svg` is an original conceptual protocol illustration, explicitly labeled as such. It is not a screenshot of an app or an upstream support claim.
- `social-preview.png` is a screenshot of this portfolio's homepage for link previews.

The supplied slide decks are not republished in full. Figure captions identify their origin. Claims about deployment, upstream merging, runtime or generalization are limited to the evidence described in each case study.
