# Codebook: kanto_battles.csv

**Description:** Battle-level dataset containing 50,000 individual battle records across Kanto.  
**Rows:** 50,000  
**Columns:** 28  
**Used in:** Chapters 3, 5, 8  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `battle_id` | int | 1–50000 | Unique battle identifier |
| `attacker_trainer_id` | int | 1–2000 | Links to kanto_trainers.csv |
| `defender_trainer_id` | int | — | Defender trainer ID (0 for wild battles) |
| `battle_type` | str | 4 types | "wild", "trainer", "gym", "elite_four" |
| `location` | str | — | Route or city name where battle occurred |
| `attacker_pokemon_species` | str | — | Attacker's Pokemon species name |
| `defender_pokemon_species` | str | — | Defender's Pokemon species name |
| `attacker_level` | int | 1–100 | Attacker Pokemon level |
| `defender_level` | int | 1–100 | Defender Pokemon level |
| `attacker_type_primary` | str | 18 types | Primary type of attacker |
| `attacker_type_secondary` | str | 18 types/None | Secondary type of attacker |
| `defender_type_primary` | str | 18 types | Primary type of defender |
| `defender_type_secondary` | str | 18 types/None | Secondary type of defender |
| `type_advantage_multiplier` | float | {0.25, 0.5, 1, 2, 4} | Type effectiveness multiplier |
| `attacker_attack` | int | 1–400 | Attacker's effective Attack stat (base + IV + EV) |
| `attacker_defense` | int | 1–400 | Attacker's effective Defense stat |
| `attacker_speed` | int | 1–400 | Attacker's effective Speed stat |
| `attacker_hp` | int | 1–500 | Attacker's effective HP stat |
| `weather` | str | 5 types | "clear", "rain", "sun", "hail", "sandstorm" |
| `terrain` | str | 5 types | "grass", "cave", "water", "urban", "mountain" |
| `held_item` | str | — | Item held by attacker: "none", "berry", "boost_item", etc. |
| `critical_hit` | bool | 0/1 | Whether a critical hit occurred |
| `moves_used` | int | 1–20 | Number of turns in the battle |
| `attacker_won` | bool | 0/1 | Whether the attacker won |
| `damage_dealt` | int | 0–2000 | Total damage dealt by attacker |

## Notes

- Links to `kanto_trainers.csv` via `attacker_trainer_id`
- Wild battles have `defender_trainer_id = 0`
- Type advantage multiplier follows Gen I mechanics
