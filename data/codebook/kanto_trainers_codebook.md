# Codebook: kanto_trainers.csv

**Description:** Primary cross-sectional dataset of 2,000 simulated Pokemon trainers with their full journey data.  
**Rows:** 2,000  
**Columns:** 42  
**Used in:** Chapters 1, 3, 4, 5, 8  
**Seed:** 151  

## Variable Definitions

### Identifiers

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `trainer_id` | int | 1–2000 | Unique trainer identifier |
| `trainer_name` | str | — | Randomly generated name |
| `hometown` | str | 10 towns | One of: Pallet, Viridian, Pewter, Cerulean, Vermilion, Lavender, Celadon, Fuchsia, Saffron, Cinnabar |

### Starter & Team Composition

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `starter_type` | str | Grass/Fire/Water | Starter Pokemon type (selection bias built in: correlated with wealth, experience) |
| `starter_species` | str | 3 values | Bulbasaur, Charmander, or Squirtle |
| `team_size` | int | 1–6 | Number of Pokemon in active party |
| `team_level_avg` | float | 5–80 | Average level of party Pokemon |
| `team_level_max` | int | 5–100 | Highest level Pokemon in party |
| `team_type_diversity` | int | 1–12 | Number of unique types represented in party |
| `has_legendary` | bool | 0/1 | Whether team includes Articuno, Zapdos, Moltres, or Mewtwo |

### Trainer Characteristics

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `trainer_experience` | float | 0–15 | Years of prior Pokemon experience |
| `play_hours` | float | 50–1500 | Total hours played |
| `strategy_score` | float | 0–100 | Composite strategic ability measure |
| `patience` | float | 0–100 | **LATENT** — Unobserved in most analyses, revealed in Ch. 6 |
| `natural_talent` | float | 0–100 | **LATENT** — Unobserved |
| `dedication` | float | 0–100 | **LATENT** — Unobserved |
| `wealth` | int | 1–5 | Poke Dollar income bracket |
| `age` | int | 10–45 | Trainer age |
| `gender` | str | M/F/NB | Gender |

### Items & Training Decisions (Treatment Variables)

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `exp_share_used` | bool | 0/1 | Used Exp. Share during journey |
| `rare_candy_count` | int | 0–30 | Number of Rare Candies used |
| `potions_purchased` | int | 0–500 | Total Potions bought |
| `held_items_equipped` | int | 0–10 | Number of unique held items used |
| `tm_count` | int | 0–50 | Number of TMs taught |
| `dept_store_spending` | float | 0–50000 | Total Poke Dollars spent at Celadon Dept Store |
| `cave_training` | bool | 0/1 | Trained in Cerulean Cave |
| `thunder_training` | bool | 0/1 | Completed Lt. Surge's Thunder Training |
| `safari_zone_visits` | int | 0–20 | Number of Safari Zone visits |

### Outcomes

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `badges_earned` | int | 0–8 | Number of gym badges earned |
| `gym_win_rate` | float | 0–1 | Overall gym battle win percentage |
| `elite_four_attempts` | int | 0–20 | Number of Elite Four attempts |
| `elite_four_wins` | int | 0–10 | Number of Elite Four completions |
| `champion_defeated` | bool | 0/1 | Whether trainer beat the Champion |
| `total_battle_wins` | int | 0–5000 | Total wild + trainer + gym battle wins |
| `completion_time_hours` | float | 10–500 | Time from start to credits |

### Hidden Pokemon Genetics (For Sensitivity Analysis)

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `team_avg_iv_total` | float | 0–186 | Average Individual Values across team — **LATENT** in most analyses |
| `team_avg_ev_total` | float | 0–510 | Average Effort Values across team — **LATENT** |

## Causal Structure (Summary)

```
wealth → dept_store_spending, starter_type, exp_share_used
trainer_experience → strategy_score, starter_type, cave_training
patience → safari_zone_visits, strategy_score
natural_talent → strategy_score, team_avg_iv_total
dedication → play_hours, potions_purchased, tm_count
strategy_score + team_level_avg + type_diversity + items → badges → elite_four outcomes
```

## Notes

- Latent variables (patience, natural_talent, dedication, IVs, EVs) are included in the CSV but should be treated as unobserved in most analyses. They are revealed for pedagogical purposes in specific chapters.
- Selection bias in `starter_type`: wealthy trainers from water-adjacent towns (Cerulean, Cinnabar) tend to choose Water; experienced trainers tend to choose Fire.
