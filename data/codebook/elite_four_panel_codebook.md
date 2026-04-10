# Codebook: elite_four_panel.csv

**Description:** Panel dataset tracking 500 trainers across 4 sequential Elite Four battles.  
**Rows:** 2,000 (500 trainers × 4 battles)  
**Columns:** 20  
**Used in:** Chapter 8 (Mediation, Dynamic Treatment Regimes)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `trainer_id` | int | 1–500 | Unique trainer identifier |
| `elite_four_member` | str | 4 values | Lorelei, Bruno, Agatha, or Lance |
| `battle_order` | int | 1–4 | Sequence position (1=Lorelei, 4=Lance) |
| `item_used_this_battle` | bool | 0/1 | **TREATMENT:** Whether trainer used items this battle |
| `pokemon_health_entering` | float | 0–100 | **MEDIATOR:** Team health % entering this battle (affected by prior battle's item use) |
| `arena_temperature` | float | -20–40 | Arena temperature (Lorelei's ice arena is cold) |
| `opponent_type_matchup_score` | float | 0–10 | How favorable the trainer's type matchup is |
| `battle_won` | bool | 0/1 | **OUTCOME:** Whether trainer won this battle |
| `damage_dealt` | int | 0–1000 | Total damage dealt |
| `damage_taken` | int | 0–1000 | Total damage received |
| `turns` | int | 1–30 | Number of battle turns |
| `fatigue_level` | float | 0–100 | **TIME-VARYING CONFOUNDER:** Increases with each battle |
| `team_morale` | float | 0–100 | **TIME-VARYING CONFOUNDER:** Affected by prior wins/losses |

## Causal Structure

- Item use at battle $t$ → Pokemon health entering battle $t+1$ (mediator) → battle $t+1$ outcome
- Fatigue and morale are **time-varying confounders affected by prior treatment**: using items at battle $t$ affects morale at $t+1$, which confounds item use at $t+1$ → outcome at $t+1$
- This creates the classic setting for Marginal Structural Models and g-computation
