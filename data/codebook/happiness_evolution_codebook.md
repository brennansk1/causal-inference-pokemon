# Codebook: happiness_evolution.csv

**Description:** Regression Discontinuity dataset from Cinnabar Island. Pokemon near the happiness evolution threshold.  
**Rows:** 800  
**Columns:** 12  
**Used in:** Chapter 6 (Regression Discontinuity Design)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `pokemon_id` | int | 1–800 | Unique Pokemon identifier |
| `species` | str | — | Pokemon species name |
| `happiness_score` | float | 150–280 | **RUNNING VARIABLE:** Continuous happiness score |
| `evolution_threshold` | int | 220 | Constant: the happiness cutoff for evolution |
| `evolved` | bool | 0/1 | Whether happiness ≥ threshold (sharp assignment) |
| `trainer_pressed_b` | bool | 0/1 | Whether trainer cancelled evolution (creates fuzzy design) |
| `actually_evolved` | bool | 0/1 | **TREATMENT:** evolved AND didn't press B |
| `battle_performance_post` | float | 0–100 | **OUTCOME:** Post-evolution/non-evolution battle score |
| `level_pre` | int | 15–50 | Pre-treatment Pokemon level |
| `attack_pre` | int | 20–150 | Pre-treatment Attack stat |
| `defense_pre` | int | 20–150 | Pre-treatment Defense stat |
| `speed_pre` | int | 20–150 | Pre-treatment Speed stat |

## RDD Structure

- **Sharp RDD:** `evolved` is a deterministic function of `happiness_score ≥ 220`
- **Fuzzy RDD:** `actually_evolved` has a jump at the threshold but not from 0 to 1 (because some trainers press B to cancel evolution)
- **Identification:** At the cutoff, Pokemon just above and just below 220 happiness are comparable on all other characteristics
- **McCrary test:** Density of `happiness_score` should be smooth at 220 (no manipulation)
- Pre-treatment covariates (`level_pre`, `attack_pre`, `defense_pre`, `speed_pre`) should show no discontinuity at the cutoff
