# Codebook: pewter_protein_rct.csv

**Description:** Experimental dataset from Pewter City's Randomized Controlled Trial of Pewter Protein supplement.  
**Rows:** 200  
**Columns:** 14  
**Used in:** Chapter 2 (Randomized Experiments)  
**Seed:** 151  

## Variable Definitions

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `trainer_id` | int | — | Unique trainer identifier (links to kanto_trainers.csv) |
| `treatment_assigned` | int | 0/1 | 1 = assigned Pewter Protein, 0 = assigned Placebo Berry |
| `treatment_received` | int | 0/1 | Actual treatment received (allows noncompliance) |
| `team_level_pre` | float | 5–30 | Pre-treatment average team level |
| `badges_pre` | int | 0–2 | Pre-treatment badges earned |
| `trainer_experience` | float | 0–15 | Years of prior experience |
| `strategy_score_pre` | float | 0–100 | Pre-treatment strategy score |
| `brock_win` | bool | 0/1 | Whether trainer defeated Brock |
| `brock_damage_dealt` | int | 0–500 | Total damage dealt to Brock's team |
| `brock_turns` | int | 1–30 | Number of turns in the Brock battle |
| `attack_stat_change` | float | -10–30 | Change in lead Pokemon's Attack stat |
| `team_has_rock_weakness` | bool | 0/1 | Whether team has Water or Grass types (blocking variable) |
| `completed_study` | bool | 0/1 | Whether trainer completed the study (attrition indicator) |
| `compliance_type` | str | 3 types | "complier", "always_taker", "never_taker" — **HIDDEN** for pedagogical reveal |

## Design Notes

- **Randomization:** Simple random assignment, 1:1 allocation
- **Noncompliance:** ~15% noncompliance rate. Some assigned Protein refused (never-takers); some assigned Placebo obtained Protein through trade (always-takers).
- **Attrition:** ~5% dropout rate (trainers who lost badly and left Pewter)
- **Blocking variable:** `team_has_rock_weakness` can be used for stratified analysis
- `compliance_type` is hidden initially; revealed in later notebook cells for LATE discussion (Ch. 6 preview)
