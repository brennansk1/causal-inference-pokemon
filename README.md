# Causal Inference: A Pokemon Approach

### Kanto Region Edition

> *Learn causal inference by journeying through Kanto.* From potential outcomes in Pallet Town to causal forests at the Indigo Plateau, this open-source textbook teaches the full spectrum of causal inference — undergraduate foundations through PhD-level frontiers — using Pokemon-themed simulated data, interactive Jupyter notebooks, and a narrative that follows the original Kanto adventure.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Textbook-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg)](https://jupyter.org/)

---

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/causal-inference-pokemon.git
cd causal-inference-pokemon
pip install -e ".[full]"
python data/dgp/generate_all.py    # Generate all datasets (seed=151)
python assets/download_sprites.py  # Fetch Pokemon sprites
jupyter notebook
```

## Chapter Map

| Ch. | Location | Topic | Notebook | Dataset |
|-----|----------|-------|----------|---------|
| 1 | Pallet Town | Potential Outcomes & Counterfactuals | [ch01](notebooks/ch01_pallet_town.ipynb) | `kanto_trainers.csv` |
| 2 | Pewter City | Randomized Experiments | [ch02](notebooks/ch02_pewter_city.ipynb) | `pewter_protein_rct.csv` |
| 3 | Cerulean City | Observational Studies & DAGs | [ch03](notebooks/ch03_cerulean_city.ipynb) | `kanto_trainers.csv`, `kanto_battles.csv` |
| 4 | Vermilion City | Matching & Propensity Scores | [ch04](notebooks/ch04_vermilion_city.ipynb) | `ss_anne_passengers.csv` |
| 5 | Celadon City | Regression, IPW & Doubly Robust | [ch05](notebooks/ch05_celadon_city.ipynb) | `kanto_trainers.csv` |
| 6 | Fuchsia & Cinnabar | Instrumental Variables & RDD | [ch06](notebooks/ch06_fuchsia_cinnabar.ipynb) | `safari_zone_lottery.csv`, `happiness_evolution.csv` |
| 7 | Saffron City | Diff-in-Diff & Synthetic Control | [ch07](notebooks/ch07_saffron_city.ipynb) | `kanto_cities_panel.csv`, `shadow_surge_staggered.csv` |
| 8 | Indigo Plateau | Advanced Topics & Frontiers | [ch08](notebooks/ch08_indigo_plateau.ipynb) | `elite_four_panel.csv`, `double_battles.csv` |

**Appendices:** [A: Math Review](textbook/chapters/appendix_a_math.md) | [B: Data & Environment](textbook/chapters/appendix_b_data.md) | [C: Full Kanto DAG](textbook/chapters/appendix_c_dag.md) | [D: Glossary](textbook/chapters/appendix_d_glossary.md)

## What You'll Learn

**Tier 1 — Undergraduate Foundations** (Chapters 1-2)
Potential outcomes, counterfactuals, ATE/ATT, RCT design, randomization inference

**Tier 2 — Upper Undergraduate / Early Graduate** (Chapters 2-5)
DAGs, d-separation, backdoor criterion, matching, propensity scores, OLS, IPW, doubly robust estimation

**Tier 3 — Graduate / Masters** (Chapters 4-7)
IV/2SLS, LATE, sharp & fuzzy RDD, difference-in-differences, TWFE, synthetic control

**Tier 4 — PhD / Frontier** (Chapters 7-8)
Modern staggered DiD (Callaway-Sant'Anna, Sun-Abraham, Goodman-Bacon), causal forests, DML, TMLE, mediation analysis, interference, causal discovery, transportability, dynamic treatment regimes

## Features

- **11 simulated datasets** with fully documented data generating processes
- **Interactive widgets**: confounder sliders, DAG builders, RDD bandwidth selectors, and more
- **Gym badge progression**: earn badges as you complete each chapter's challenges
- **Rival Blue**: a recurring character who makes causal fallacies for you to identify
- **Professor Oak**: guides you through formal definitions and mathematical foundations
- **Reproducible**: `seed=151` everywhere, conda environment, CI-validated notebooks

## Project Structure

```
causal-inference-pokemon/
├── textbook/chapters/     # 8 chapters + 4 appendices (Markdown + LaTeX)
├── notebooks/             # Interactive Jupyter notebooks
├── data/
│   ├── raw/               # Generated datasets (CSV)
│   ├── codebook/          # Data dictionaries
│   └── dgp/               # Data generating process scripts
├── src/kanto_utils/       # Helper package (data loading, plotting, estimators)
├── assets/                # Sprites, maps, badges, diagrams, matplotlib theme
└── tests/                 # Unit tests
```

## Estimated Learning Time

| Tier | Chapters | Reading | Notebooks | Total |
|------|----------|---------|-----------|-------|
| Undergraduate | 1-2 | ~6 hrs | ~4 hrs | **10 hrs** |
| Upper Undergrad | 3-5 | ~10 hrs | ~8 hrs | **18 hrs** |
| Graduate | 6-7 | ~8 hrs | ~8 hrs | **16 hrs** |
| PhD / Frontier | 8 | ~8 hrs | ~6 hrs | **14 hrs** |
| **Total** | | | | **~58 hrs** |

Approximately one semester at 4 hours/week.

## Pokemon Disclaimer

Pokemon is owned by Nintendo, Game Freak, and Creatures Inc. All Pokemon names, sprites, and related imagery are trademarks of their respective owners. This project uses Pokemon references for **educational purposes only**. Sprite assets are fetched via download scripts from community repositories (PokeAPI) and are not bundled in this repository.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

- **Textbook content**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **Source code**: [MIT](https://opensource.org/licenses/MIT)
