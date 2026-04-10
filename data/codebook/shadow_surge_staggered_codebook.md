# Codebook: shadow_surge_staggered.csv

**Description:** Staggered Difference-in-Differences dataset. 8 Kanto cities with staggered Shadow Surge TM adoption.  
**Rows:** 192 (8 cities × 24 periods)  
**Columns:** 15  
**Used in:** Chapter 7 (Staggered DiD, Modern DiD Methods)  
**Seed:** 151  

## Variable Definitions

Same schema as `kanto_cities_panel.csv` (see that codebook) with specific staggered adoption timing.

## Staggered Adoption Schedule

| City | Adoption Period | Group |
|------|----------------|-------|
| Saffron | Period 6 | Early adopter |
| Cerulean | Period 10 | Mid-early adopter |
| Vermilion | Period 14 | Mid-late adopter |
| Lavender | Period 18 | Late adopter |
| Celadon | Never | Control |
| Fuchsia | Never | Control |
| Pewter | Never | Control |
| Cinnabar | Never | Control |

## Key Design Features

- **Heterogeneous treatment effects:** The treatment effect varies across cities and grows over time (this is what makes naive TWFE biased)
- **Negative weighting:** Standard TWFE regression produces comparisons where early adopters serve as "controls" for late adopters, producing negative weights
- **Parallel trends:** Pre-treatment trends are parallel across all 8 cities (by construction)
- Used to demonstrate: Goodman-Bacon decomposition, Callaway-Sant'Anna, Sun-Abraham, de Chaisemartin-D'Haultfoeuille estimators
