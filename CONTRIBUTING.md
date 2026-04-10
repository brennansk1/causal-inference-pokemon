# Contributing to Causal Inference: A Pokemon Approach

Thanks for your interest in contributing! This project welcomes contributions of all kinds.

## Ways to Contribute

- **Bug reports**: Found an error in a formula, code, or dataset? Open an issue.
- **Typo fixes**: Submit a PR directly for small text corrections.
- **New exercises**: Propose additional challenge exercises for any chapter.
- **Notebook improvements**: Better visualizations, clearer explanations, new widgets.
- **Dataset enhancements**: Improvements to the data generating process.
- **Translations**: Help translate chapters to other languages.

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/causal-inference-pokemon.git
cd causal-inference-pokemon
pip install -e ".[dev,full]"
python data/dgp/generate_all.py
jupyter notebook
```

## Style Guide

### Code
- Follow PEP 8 for Python code
- Use type hints for function signatures in `kanto_utils`
- All notebooks should run top-to-bottom without errors
- Use `seed=151` for all random operations (the original 151 Pokemon)

### Writing
- Use Pokemon analogies consistently — check the glossary (Appendix D)
- Mathematical notation follows the conventions in Appendix A
- Every new concept gets: (1) intuition, (2) formal definition, (3) Pokemon example
- Callout boxes use the established patterns: "Professor Oak explains...", "Rival Blue says..."

### Commits
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- One logical change per commit

## Pull Request Process

1. Fork the repo and create a feature branch
2. Make your changes
3. Ensure all notebooks run without errors: `pytest tests/`
4. Update the CHANGELOG.md if applicable
5. Submit a PR with a clear description

## Code of Conduct

Be respectful and constructive. We're all here to learn causal inference (and catch 'em all).
