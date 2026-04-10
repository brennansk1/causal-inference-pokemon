# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [1.0.0] - 2026-04-10

### Added
- Complete textbook: 8 chapters + 4 appendices covering causal inference from undergraduate to PhD level (~99k words)
- Full 202-page textbook PDF at `textbook/build/output/causal_inference_pokemon.pdf`
- 12 Jupyter notebooks (378 cells total) with interactive widgets and exercises
- 11 simulated datasets with fully documented data generating processes
- `kanto_utils` helper package (2,300 lines) for data loading, plotting, and causal estimation
- 10 causal estimators: difference-in-means, randomization inference, propensity score, IPW, doubly robust, Wald, 2SLS, sharp RDD, 2x2 DiD, balance table
- 4 interactive widgets: confounder slider, RDD bandwidth slider, power analysis, starter selector
- Custom matplotlib Kanto theme
- Pokemon reference data: 151-entry Kanto Pokedex, base stats, type effectiveness matrix
- 11 codebooks documenting each dataset
- Asset download scripts for Pokemon sprites from PokeAPI
- GitHub Actions CI/CD for tests, notebook validation, and PDF builds
- Review process (REVIEW.md), PR template, CODEOWNERS file
- Trainer Card progress tracker
