# Codebook: johto_transportability.csv

**Description:** Transportability dataset with 1,000 Johto region trainers. Same schema as kanto_trainers.csv but different covariate distributions.  
**Rows:** 1,000  
**Columns:** 42  
**Used in:** Chapter 8 (Transportability & External Validity)  
**Seed:** 151  

## Variable Definitions

Same 42-column schema as `kanto_trainers.csv` with the following differences:

### Key Distribution Differences from Kanto

| Variable | Kanto | Johto |
|----------|-------|-------|
| `starter_species` | Bulbasaur/Charmander/Squirtle | Chikorita/Cyndaquil/Totodile |
| `hometown` | 10 Kanto towns | 10 Johto towns (New Bark, Cherrygrove, Violet, Azalea, Goldenrod, Ecruteak, Olivine, Cianwood, Mahogany, Blackthorn) |
| `trainer_experience` | Higher average | Lower average (newer region) |
| `wealth` | Moderate distribution | Shifted (Goldenrod is wealthier) |
| `team_type_diversity` | Gen I types | Gen I+II types available |

## Purpose

- Tests whether causal estimates from Kanto data **transport** to Johto
- Different covariate distributions mean effect modifiers can shift the ATE
- Used with selection diagrams (Bareinboim & Pearl 2013) and reweighting methods
- Students compare naive extrapolation to formally transported estimates
