# Codebook: kanto_cities_panel.csv

**Description:** City-level panel data tracking 8 Kanto cities across 24 monthly periods.  
**Rows:** 192 (8 cities × 24 periods)  
**Columns:** 15  
**Used in:** Chapter 7 (Difference-in-Differences, Synthetic Control)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `city_id` | int | 1–8 | Unique city identifier |
| `city_name` | str | 8 cities | Pewter, Cerulean, Vermilion, Lavender, Celadon, Fuchsia, Saffron, Cinnabar |
| `period` | int | 1–24 | Time period (each = 1 month) |
| `avg_win_rate` | float | 0–1 | City-level average trainer win rate |
| `avg_trainer_level` | float | 1–80 | Mean Pokemon level among city's trainers |
| `trainer_population` | int | 50–500 | Number of active trainers in city |
| `gym_difficulty` | float | 1–10 | Difficulty rating of local gym |
| `economic_index` | float | 50–150 | City economic activity (100 = baseline) |
| `shadow_surge_available` | bool | 0/1 | Whether Shadow Surge TM is available |
| `shadow_surge_adoption_period` | int | — | Period when TM became available (0 = never) |
| `team_rocket_presence` | bool | 0/1 | Whether Team Rocket is active in city |
| `team_rocket_invasion_period` | int | — | Period of invasion start (0 = never) |
| `pokemart_items_available` | int | 10–100 | Count of items in local Poke Mart |
| `pokemon_center_visits` | int | 100–5000 | Monthly Pokemon Center traffic |
| `avg_potion_price` | float | 100–500 | Price index for healing items |

## Treatment Events

- **Shadow Surge TM:** Released first in Saffron City, then staggered to other cities
- **Team Rocket Invasion:** Saffron City invaded; used for Synthetic Control analysis

## Notes

- Panel structure: city × time
- Parallel trends can be visually assessed in pre-treatment periods
- Shadow Surge staggered adoption creates the setting for modern DiD methods (see `shadow_surge_staggered.csv` for the explicit staggered design)
