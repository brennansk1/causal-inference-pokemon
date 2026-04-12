# Audiobook: Causal Inference -- A Pokemon Approach

Audio edition of the textbook, generated from adapted chapter scripts using Kokoro TTS.

## Quick Start

```bash
# Install dependencies
brew install espeak-ng ffmpeg
pip install kokoro soundfile numpy pydub mutagen pyyaml

# Preview (no audio generated)
python generate_audiobook.py --dry-run

# Generate all chapters
python generate_audiobook.py

# Generate a single chapter
python generate_audiobook.py --chapter ch01

# Resume after interruption
python generate_audiobook.py --resume

# Combine into one file
python generate_audiobook.py --combine
```

## Chapter List

| # | File | Title | Est. Runtime |
|---|---|---|---|
| 1 | `00_front_matter.md` | Introduction & How to Listen | ~10 min |
| 2 | `ch01_pallet_town.md` | Pallet Town: What Is Causal Inference? | ~60 min |
| 3 | `ch02_pewter_city.md` | Pewter City: Randomized Experiments | ~70 min |
| 4 | `ch03_cerulean_city.md` | Cerulean City: Observational Studies & DAGs | ~90 min |
| 5 | `ch04_vermilion_city.md` | Vermilion City: Matching & Propensity Scores | ~75 min |
| 6 | `ch05_celadon_city.md` | Celadon City: Regression, IPW & Doubly Robust | ~70 min |
| 7 | `ch06_fuchsia_cinnabar.md` | Fuchsia & Cinnabar: IV & RDD | ~85 min |
| 8 | `ch07_saffron_city.md` | Saffron City: DiD & Synthetic Control | ~80 min |
| 9 | `ch08_indigo_plateau.md` | Indigo Plateau: Advanced Topics & Frontiers | ~100 min |
| 10 | `appendix_math_foundations.md` | Mathematical Foundations | ~40 min |
| 11 | `appendix_causal_pokedex.md` | The Causal Pokedex | ~20 min |

**Total: ~12-13 hours**

## Voices

| Role | Kokoro Voice | Speed |
|---|---|---|
| Narrator | `am_michael` | 0.90 |
| Professor Oak | `bm_george` | 0.88 |
| Blue / Male supporting | `am_adam` | 0.95 |
| Female characters | `af_heart` | 0.90 |

## Structure

```
audiobook/
  generate_audiobook.py       # TTS generation script
  scripts/                    # Adapted chapter scripts (11 files)
  templates/                  # Script template + transformation patterns
  production/                 # Character guide, pronunciation guide
  output/
    wav/                      # Intermediate WAV files
    mp3/                      # Final MP3 output
    progress.json             # Resume tracking
    manifest.json             # Track metadata
```
