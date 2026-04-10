# Codebook: ss_anne_passengers.csv

**Description:** Matching dataset from the S.S. Anne cruise. 400 trainers, some of whom completed Lt. Surge's Thunder Training.  
**Rows:** 400  
**Columns:** 16  
**Used in:** Chapter 4 (Matching & Subclassification)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `passenger_id` | int | 1–400 | Unique passenger identifier |
| `thunder_training` | bool | 0/1 | **TREATMENT:** Completed Lt. Surge's Thunder Training program |
| `badges` | int | 0–8 | Gym badges earned at time of boarding |
| `team_level_avg` | float | 5–60 | Average team Pokemon level |
| `trainer_experience` | float | 0–15 | Years of prior experience |
| `play_hours` | float | 50–800 | Total hours played |
| `starter_type` | str | 3 types | Grass, Fire, or Water |
| `team_size` | int | 1–6 | Number of Pokemon in party |
| `strategy_score` | float | 0–100 | Strategic ability measure |
| `wealth` | int | 1–5 | Income bracket |
| `age` | int | 10–45 | Trainer age |
| `vermilion_gym_win` | bool | 0/1 | **OUTCOME:** Whether trainer beat Lt. Surge's gym |
| `surge_battle_damage` | int | 0–500 | **OUTCOME:** Damage dealt in Surge battle |
| `patience` | float | 0–100 | **HIDDEN CONFOUNDER** — unobserved, revealed later |
| `natural_talent` | float | 0–100 | **HIDDEN CONFOUNDER** — unobserved, revealed later |
| `saw_surge_ad` | bool | 0/1 | Saw advertisement for Thunder Training |
| `friend_recommended` | bool | 0/1 | Had a friend recommend the program |

## Causal Structure

- Thunder Training selection is confounded by experience, strategy, badges, and the **hidden** confounders patience and natural_talent
- `saw_surge_ad` and `friend_recommended` drive treatment uptake but may not satisfy exclusion restriction
- The hidden confounders are revealed in later notebook cells to demonstrate the limits of selection-on-observables
