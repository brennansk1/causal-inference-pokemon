# Codebook: safari_zone_lottery.csv

**Description:** Instrumental variable dataset from Fuchsia City's Safari Zone lottery system.  
**Rows:** 600  
**Columns:** 12  
**Used in:** Chapter 6 (Instrumental Variables)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `trainer_id` | int | 1–600 | Unique trainer identifier |
| `lottery_won` | bool | 0/1 | **INSTRUMENT:** Won the Safari Zone free pass lottery |
| `safari_attended` | bool | 0/1 | **TREATMENT:** Actually attended the Safari Zone |
| `battle_wins_post` | int | 0–100 | **OUTCOME:** Post-Safari battle win count |
| `badges` | int | 0–8 | Gym badges earned |
| `team_level_avg` | float | 5–60 | Average team level |
| `trainer_experience` | float | 0–15 | Years of experience |
| `patience` | float | 0–100 | **UNOBSERVED CONFOUNDER** — revealed for pedagogy |
| `compliance_type` | str | 3 types | "complier", "always_taker", "never_taker" |
| `first_stage_strength` | float | 0–1 | How much lottery affects attendance (varies by subgroup) |

## IV Structure

```
lottery_won (Z) ──→ safari_attended (D) ──→ battle_wins_post (Y)
                                ↑                     ↑
                            patience (U) ─────────────┘
```

- **Instrument (Z):** `lottery_won` — randomly assigned, ~50% win rate
- **Treatment (D):** `safari_attended` — affected by lottery AND patience
- **Outcome (Y):** `battle_wins_post` — affected by Safari attendance AND patience
- **Unobserved confounder (U):** `patience` — patient trainers attend Safari Zone more AND win more battles

## Compliance Types

- **Compliers** (~60%): Attend only if they win the lottery
- **Always-Takers** (~25%): Attend regardless (patient, dedicated trainers)
- **Never-Takers** (~15%): Never attend regardless (busy trainers)
- **Defiers** (0%): None by monotonicity assumption
