# Codebook: double_battles.csv

**Description:** Interference/spillover dataset from 1,000 double battles where two Pokemon fight simultaneously.  
**Rows:** 1,000  
**Columns:** 14  
**Used in:** Chapter 8 (Interference & Spillovers)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `battle_id` | int | 1–1000 | Unique battle identifier |
| `trainer_id` | int | — | Trainer ID |
| `pokemon_1_species` | str | — | First Pokemon on field |
| `pokemon_2_species` | str | — | Second Pokemon on field |
| `pokemon_1_move_used` | str | — | Move used by Pokemon 1 |
| `pokemon_2_move_used` | str | — | Move used by Pokemon 2 |
| `move_1_hits_partner` | bool | 0/1 | Whether Pokemon 1's move hits its partner (e.g., Earthquake, Surf) |
| `pokemon_1_damage` | int | 0–500 | Damage dealt by Pokemon 1 to opponent |
| `pokemon_2_damage` | int | 0–500 | Damage dealt by Pokemon 2 to opponent |
| `pokemon_1_won` | bool | 0/1 | Whether Pokemon 1 defeated its target |
| `pokemon_2_won` | bool | 0/1 | Whether Pokemon 2 defeated its target |
| `battle_won` | bool | 0/1 | Whether the overall battle was won |
| `partner_interference_magnitude` | float | 0–100 | Continuous measure of how much Pokemon 1's action affected Pokemon 2 |

## Interference Structure

- **SUTVA violation:** Pokemon 1's move choice affects Pokemon 2's outcome (and vice versa)
- **Example:** Using Earthquake deals damage to the opponent AND your partner
- Illustrates: direct effects, indirect (spillover) effects, total effects, overall effects
- Demonstrates why standard causal estimators fail under interference
