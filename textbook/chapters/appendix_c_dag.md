# Appendix C: The Full Kanto Causal DAG

---

*Deep in Professor Oak's study, behind a locked door that opens only after you have earned all eight badges, there is a wall-sized diagram. Strings connect photographs of trainers, items, and Pokemon. Arrows are drawn in red marker. Post-it notes list equations. "This," says Professor Oak, pulling back the curtain, "is the true structure of the world --- the causal graph that governs how trainers succeed or fail in Kanto. Every association you have observed, every confound you have struggled with, every backdoor path you have blocked --- it all comes from here."*

---

## C.1 Overview

The **Kanto Causal DAG** is the directed acyclic graph (DAG) that describes the data-generating process (DGP) for the primary dataset, `kanto_trainers.csv`. Every variable in that dataset is a node, and every causal arrow is derived from the structural equations in `data/dgp/structural_equations.py`.

This DAG serves three roles:

1. **Ground truth** for the textbook exercises. Because the data is synthetic, the DAG *is* the correct causal model. Students can verify whether their identification strategies target the right adjustment sets.
2. **Reference for instructors** designing exam questions or alternative exercises.
3. **Worked example** of how a complex causal graph is documented, analyzed, and used in practice.

---

## C.2 Node Inventory

### Latent (Unobserved) Nodes

These variables exist in the DGP and appear in the CSV for pedagogical transparency, but in the "story" of the textbook they are initially hidden from the researcher. In DAG diagrams, they are drawn with **dashed borders** or rendered in **gray**.

| Node | Range | Description |
|:---|:---:|:---|
| `patience` | 0--100 | Innate patience of the trainer. Affects strategic thinking and willingness to grind. Drawn from $\text{Uniform}(0, 100)$. |
| `natural_talent` | 0--100 | Raw aptitude for Pokemon battling. Affects team IVs and strategy. Drawn from $\text{Uniform}(0, 100)$. |
| `dedication` | 0--100 | Long-term commitment to training. Affects hours played and items purchased. Drawn from $\text{Uniform}(0, 100)$. |

### Observed Nodes: Background Characteristics

| Node | Type | Range | Description |
|:---|:---:|:---:|:---|
| `trainer_id` | ID | 1--2000 | Unique identifier. Not a causal variable. |
| `trainer_name` | ID | string | Unique name. Not a causal variable. |
| `hometown` | Categorical | 10 Kanto towns | Where the trainer grew up. Exogenous. |
| `hometown_gym_type` | Categorical | 10 types + "None" | Deterministic function of `hometown`. |
| `region` | Constant | "Kanto" | Always "Kanto" in this dataset. |

### Observed Nodes: Trainer Attributes

| Node | Type | Range | Description |
|:---|:---:|:---:|:---|
| `wealth` | Ordinal | 1--5 | Socioeconomic status. Influenced by `hometown`. |
| `trainer_experience` | Continuous | 0--15 | Years of training experience. Exogenous (drawn from Exponential). |
| `play_hours` | Count | 10--999 | Total hours played. Driven by `dedication` and `trainer_experience`. |
| `strategy_score` | Continuous | 0--100 | Composite measure of battle strategy. Driven by `patience`, `natural_talent`, and `trainer_experience`. |
| `cave_training` | Binary | 0/1 | Whether the trainer trained in caves. Driven by `trainer_experience` and `dedication`. |
| `safari_zone_visits` | Count | 0--30 | Number of Safari Zone trips. Driven by `patience`. |
| `fishing_attempts` | Count | 0--50 | Number of fishing attempts. Driven by `patience`. |

### Observed Nodes: Starter and Team

| Node | Type | Range | Description |
|:---|:---:|:---:|:---|
| `starter_type` | Categorical | Grass/Fire/Water | Starter choice. Influenced by `wealth` (Fire bias) and `trainer_experience` (Water bias). |
| `starter_species` | Categorical | Bulbasaur/Charmander/Squirtle | Deterministic function of `starter_type`. |
| `team_size` | Count | 1--6 | Number of Pokemon on team. Driven by `trainer_experience`. |
| `team_level_avg` | Continuous | 5--100 | Average level of team. Driven by `trainer_experience` and `dedication`. |
| `team_level_max` | Continuous | 5--100 | Maximum level on team. Driven by `team_level_avg`. |
| `team_avg_iv_total` | Continuous | 0--186 | Average IV total across team. Driven by `natural_talent`. |
| `team_avg_ev_total` | Continuous | 0--510 | Average EV total. Driven by `play_hours` and `cave_training`. |
| `type_diversity` | Count | 1--6 | Number of distinct types on team. Driven by `trainer_experience` and `patience`. |
| `team_happiness_avg` | Continuous | 0--255 | Average happiness. Driven by `patience` and `dedication`. |
| `team_friendship_max` | Continuous | 0--255 | Max friendship. Driven by `team_happiness_avg`. |

### Observed Nodes: Items and Spending

| Node | Type | Range | Description |
|:---|:---:|:---:|:---|
| `dept_store_spending` | Continuous | 0--10000 | Pokedollars spent at Celadon Dept. Store. Driven by `wealth` and `play_hours`. |
| `potions_purchased` | Count | 0--200 | Total potions bought. Driven by `dedication` and `play_hours`. |
| `revives_used` | Count | 0--50 | Total revives used. Driven by `play_hours`. |
| `tm_count` | Count | 0--50 | Number of TMs collected. Driven by `dedication` and `trainer_experience`. |
| `exp_share_used` | Binary | 0/1 | Whether Exp. Share was used. Driven by `wealth` and `trainer_experience`. |
| `held_item_count` | Count | 0--6 | Number of held items. Driven by `wealth` and `tm_count`. |
| `rare_candy_used` | Count | 0--20 | Rare candies consumed. Driven by `wealth`. |
| `gym_pokemon_center_visits` | Count | 0--100 | Pokemon Center visits. Driven by `play_hours`. |
| `traded_pokemon_count` | Count | 0--15 | Pokemon received via trade. Driven by `trainer_experience`. |

### Observed Nodes: Outcomes

| Node | Type | Range | Description |
|:---|:---:|:---:|:---|
| `badges` | Count | 0--8 | Gym badges earned. **Primary outcome**. |
| `elite_four_attempted` | Binary | 0/1 | Deterministic: 1 iff `badges == 8`. |
| `elite_four_wins` | Binary | 0/1 | Won the Elite Four challenge. |
| `champion_defeated` | Binary | 0/1 | Defeated the Champion. |
| `hall_of_fame_time` | Continuous | NaN or hours | Time to Hall of Fame (NaN if not Champion). |
| `total_battles_won` | Count | 0--999 | Total battle victories. |
| `total_pokemon_caught` | Count | 1--151 | Pokemon caught. |
| `pokedex_completion` | Continuous | 0--100 | Percent of Pokedex completed. |

---

## C.3 Complete Edge List

Each arrow below represents a direct causal effect in the structural equations. The format is `Parent --> Child` with a brief justification and the functional form.

### Edges from Exogenous/Latent Sources

| Edge | Justification | Functional Form |
|:---|:---|:---|
| `hometown` $\to$ `wealth` | Wealthier towns (Celadon, Saffron) give +0.3 bonus | $\text{wealth} \sim \text{round}(N(3.0 + \text{bonus}, 0.8))$, clipped 1--5 |
| `patience` $\to$ `strategy_score` | Patient trainers think before acting | $+0.25 \times \text{patience}$ |
| `patience` $\to$ `safari_zone_visits` | Patient trainers tolerate Safari Zone frustration | $\text{Poisson}(1 + 0.04 \times \text{patience})$ |
| `patience` $\to$ `fishing_attempts` | Fishing requires patience | $\text{Poisson}(3 + 0.03 \times \text{patience})$ |
| `patience` $\to$ `type_diversity` | Patient trainers build balanced teams | $+0.01 \times \text{patience}$ in Poisson rate |
| `patience` $\to$ `team_happiness_avg` | Patient trainers raise happier Pokemon | $+0.3 \times \text{patience}$ |
| `natural_talent` $\to$ `strategy_score` | Talent aids strategic thinking | $+0.3 \times \text{natural\_talent}$ |
| `natural_talent` $\to$ `team_avg_iv_total` | Talented trainers identify strong Pokemon | $+0.4 \times \text{natural\_talent}$ |
| `dedication` $\to$ `play_hours` | Dedicated trainers play more | $+5 \times \text{dedication}$ |
| `dedication` $\to$ `potions_purchased` | Dedicated trainers stock up | $+0.3 \times \text{dedication}$ |
| `dedication` $\to$ `tm_count` | Dedicated trainers seek TMs | $+0.1 \times \text{dedication}$ |
| `dedication` $\to$ `cave_training` | Dedicated trainers do hard training | $+0.02 \times \text{dedication}$ in logit |
| `dedication` $\to$ `team_happiness_avg` | Dedication breeds Pokemon happiness | $+0.2 \times \text{dedication}$ |
| `dedication` $\to$ `team_level_avg` | Dedicated trainers level up more | $+0.15 \times \text{dedication}$ |

### Edges from `trainer_experience`

| Edge | Justification | Functional Form |
|:---|:---|:---|
| `trainer_experience` $\to$ `strategy_score` | Experience improves strategy | $+1.5 \times \text{experience}$ |
| `trainer_experience` $\to$ `starter_type` | Experienced trainers favor Water (meta) | $+0.12 \times (\text{exp} - 4)$ in Water utility |
| `trainer_experience` $\to$ `team_size` | Experienced trainers fill their team | $+0.1 \times \text{experience}$ in Poisson rate |
| `trainer_experience` $\to$ `team_level_avg` | More years $\to$ higher levels | $+3 \times \text{experience}$ |
| `trainer_experience` $\to$ `type_diversity` | Experienced trainers diversify | $+0.03 \times \text{experience}$ in Poisson rate |
| `trainer_experience` $\to$ `play_hours` | More years $\to$ more hours | $+10 \times \text{experience}$ |
| `trainer_experience` $\to$ `cave_training` | Experienced trainers explore caves | $+0.15 \times \text{experience}$ in logit |
| `trainer_experience` $\to$ `tm_count` | Experience helps find TMs | $+0.3 \times \text{experience}$ |
| `trainer_experience` $\to$ `exp_share_used` | Experienced trainers know about Exp. Share | $+0.1 \times \text{experience}$ in logit |
| `trainer_experience` $\to$ `traded_pokemon_count` | Experienced trainers trade more | $+0.05 \times \text{experience}$ in Poisson rate |
| `trainer_experience` $\to$ `total_battles_won` | Experience wins battles | $+8 \times \text{experience}$ |

### Edges from `wealth`

| Edge | Justification | Functional Form |
|:---|:---|:---|
| `wealth` $\to$ `starter_type` | Wealthy trainers lean toward Fire | $+0.15 \times (\text{wealth} - 3)$ in Fire utility |
| `wealth` $\to$ `dept_store_spending` | More money $\to$ more spending | $+500 \times \text{wealth}$ |
| `wealth` $\to$ `exp_share_used` | Exp. Share costs money | $+0.4 \times (\text{wealth} - 3)$ in logit |
| `wealth` $\to$ `held_item_count` | Wealthy trainers buy held items | $+0.1 \times \text{wealth}$ in Poisson rate |
| `wealth` $\to$ `rare_candy_used` | Rare candies are expensive | $+0.15 \times (\text{wealth} - 1)$ in Poisson rate |

### Edges among Intermediates

| Edge | Justification | Functional Form |
|:---|:---|:---|
| `play_hours` $\to$ `dept_store_spending` | More playtime $\to$ more spending opportunities | $+50 \times \text{play\_hours} \times 0.01$ |
| `play_hours` $\to$ `potions_purchased` | More playtime $\to$ more potion needs | $+0.05 \times \text{play\_hours}$ |
| `play_hours` $\to$ `revives_used` | More playtime $\to$ more fainting events | $+0.02 \times \text{play\_hours}$ in Poisson rate |
| `play_hours` $\to$ `gym_pokemon_center_visits` | More playtime $\to$ more healing | $+0.1 \times \text{play\_hours}$ in Poisson rate |
| `play_hours` $\to$ `team_avg_ev_total` | More battles $\to$ more EVs | $+2 \times \text{play\_hours} \times 0.1$ |
| `play_hours` $\to$ `total_pokemon_caught` | More time $\to$ more catches | $+0.1 \times \text{play\_hours}$ |
| `cave_training` $\to$ `team_avg_ev_total` | Cave grinding gives EVs | $+1.5 \times \text{cave\_training} \times 50$ |
| `tm_count` $\to$ `held_item_count` | TM knowledge correlates with item usage | $+0.05 \times \text{tm\_count}$ in Poisson rate |
| `safari_zone_visits` $\to$ `total_pokemon_caught` | Safari catches add to total | $+2 \times \text{safari\_zone\_visits}$ |
| `team_level_avg` $\to$ `team_level_max` | Max level is above average | $\text{team\_level\_avg} + \text{Exp}(8)$ |
| `team_happiness_avg` $\to$ `team_friendship_max` | Max friendship is above average | $\text{team\_happiness\_avg} + \text{Exp}(15)$ |
| `total_pokemon_caught` $\to$ `pokedex_completion` | Deterministic: $\text{caught}/151 \times 100$ | Deterministic |

### Edges into `badges` (Primary Outcome)

The badge count is the central outcome variable. Its structural equation is:

$$
\text{badge\_logit} = -4.0 + 0.04 \times \text{strategy\_score} + 0.03 \times \text{team\_level\_avg} + 0.15 \times \text{type\_diversity} + 0.01 \times \text{tm\_count} + 0.005 \times \frac{\text{dept\_store\_spending}}{100} + 0.3 \times \text{exp\_share\_used} + 0.01 \times \text{held\_item\_count}
$$

$$
\text{badges} = \text{clip}\!\left(\lfloor \sigma(\text{badge\_logit}) \times 9 + \varepsilon \rfloor, \, 0, \, 8\right), \quad \varepsilon \sim N(0, 0.6)
$$

| Edge | Effect Direction | Coefficient |
|:---|:---:|:---:|
| `strategy_score` $\to$ `badges` | + | 0.04 |
| `team_level_avg` $\to$ `badges` | + | 0.03 |
| `type_diversity` $\to$ `badges` | + | 0.15 |
| `tm_count` $\to$ `badges` | + | 0.01 |
| `dept_store_spending` $\to$ `badges` | + | 0.005/100 |
| `exp_share_used` $\to$ `badges` | + | 0.30 |
| `held_item_count` $\to$ `badges` | + | 0.01 |

### Edges into Post-Badge Outcomes

| Edge | Justification |
|:---|:---|
| `badges` $\to$ `elite_four_attempted` | Deterministic: must have 8 badges |
| `elite_four_attempted` $\to$ `elite_four_wins` | Can only win if you attempt |
| `strategy_score` $\to$ `elite_four_wins` | Strategy helps win E4 |
| `team_level_avg` $\to$ `elite_four_wins` | Level advantage matters |
| `type_diversity` $\to$ `elite_four_wins` | Diverse teams handle E4 better |
| `tm_count` $\to$ `elite_four_wins` | More TMs = more coverage |
| `natural_talent` $\to$ `elite_four_wins` | Talent matters at highest level |
| `elite_four_wins` $\to$ `champion_defeated` | Must beat E4 first |
| `champion_defeated` $\to$ `hall_of_fame_time` | Only Champions get a time |
| `play_hours` $\to$ `hall_of_fame_time` | More hours = longer to Hall of Fame |
| `strategy_score` $\to$ `total_battles_won` | Strategy wins battles |
| `team_level_avg` $\to$ `total_battles_won` | Level wins battles |

---

## C.4 Adjustment Set Reference

For the most common treatment-outcome pairs analyzed in the textbook, the following table lists valid adjustment sets that satisfy the backdoor criterion. "Minimal" means no proper subset also satisfies the criterion.

### Treatment: `exp_share_used` --- Outcome: `badges`

**Confounders:** `wealth` (affects both Exp. Share adoption and badges through `dept_store_spending` and `held_item_count`) and `trainer_experience` (affects Exp. Share adoption and badges through multiple paths).

| Adjustment Set | Type | Notes |
|:---|:---:|:---|
| {`wealth`, `trainer_experience`} | Minimal | Blocks all backdoor paths. Preferred. |
| {`wealth`, `trainer_experience`, `strategy_score`} | Valid | Over-controlling, but not harmful. |
| {`wealth`, `trainer_experience`, `team_level_avg`} | Valid | `team_level_avg` is a mediator via `trainer_experience`, but since `trainer_experience` is already included, no bias. |
| {`strategy_score`} alone | **Invalid** | Does not block `wealth` $\to$ `exp_share_used` path. |
| {`badges`} | **Invalid** | Outcome; never condition on the outcome. |
| {`dept_store_spending`} | **Invalid** | Descendant of `wealth` on a causal path to `badges`; conditioning opens alternative paths. |

### Treatment: `starter_type` --- Outcome: `badges`

**Confounders:** `wealth` (Fire bias, spending), `trainer_experience` (Water bias, team strength).

| Adjustment Set | Type | Notes |
|:---|:---:|:---|
| {`wealth`, `trainer_experience`} | Minimal | Blocks both backdoor paths. |
| {`wealth`, `trainer_experience`, `patience`, `natural_talent`, `dedication`} | Valid | Latents are not confounders for this pair, but conditioning on them is harmless. |
| {`strategy_score`} alone | **Invalid** | Mediator. `trainer_experience` $\to$ `strategy_score` $\to$ `badges`. Controlling for it blocks a causal pathway *and* fails to block the `wealth` path. |
| {} (empty) | **Invalid** | Both `wealth` and `experience` confound. |

### Treatment: `cave_training` --- Outcome: `badges`

**Confounders:** `trainer_experience` and `dedication` (both drive `cave_training` and affect `badges` through team levels and strategy).

| Adjustment Set | Type | Notes |
|:---|:---:|:---|
| {`trainer_experience`, `dedication`} | Minimal | `dedication` is latent but included in data for analysis. |
| {`trainer_experience`} alone | **Partial** | Blocks `experience` path but leaves `dedication` unblocked. Biased unless `dedication` is also included. |

### Treatment: `safari_zone_visits` --- Outcome: `total_pokemon_caught`

**Confounder:** `patience` (drives Safari visits and, indirectly through play habits, total catches).

| Adjustment Set | Type | Notes |
|:---|:---:|:---|
| {`patience`} | Minimal | Blocks the sole backdoor path. |
| {`patience`, `play_hours`} | Valid | `play_hours` is not a confounder here (no direct path from `patience` to `play_hours`), so adding it is harmless. |

---

## C.5 Path Analysis for Key Treatment-Outcome Pairs

### `exp_share_used` $\to$ `badges`

**Causal (directed) paths:**

1. `exp_share_used` $\to$ `badges` (direct effect, coefficient 0.30)

**Backdoor paths (non-causal, through common causes):**

1. `exp_share_used` $\leftarrow$ `wealth` $\to$ `dept_store_spending` $\to$ `badges`
2. `exp_share_used` $\leftarrow$ `wealth` $\to$ `held_item_count` $\to$ `badges`
3. `exp_share_used` $\leftarrow$ `wealth` $\to$ `starter_type` $\leftarrow$ `trainer_experience` $\to$ `strategy_score` $\to$ `badges` (this path contains a collider at `starter_type`, so it is **blocked** by default)
4. `exp_share_used` $\leftarrow$ `trainer_experience` $\to$ `strategy_score` $\to$ `badges`
5. `exp_share_used` $\leftarrow$ `trainer_experience` $\to$ `team_level_avg` $\to$ `badges`
6. `exp_share_used` $\leftarrow$ `trainer_experience` $\to$ `type_diversity` $\to$ `badges`
7. `exp_share_used` $\leftarrow$ `trainer_experience` $\to$ `tm_count` $\to$ `badges`

**Blocking strategy:** Condition on {`wealth`, `trainer_experience`}. This blocks paths 1, 2, 4, 5, 6, and 7. Path 3 is already blocked by the collider at `starter_type` (and remains blocked as long as we do not condition on `starter_type`).

### `starter_type` $\to$ `badges`

**Causal (directed) paths:**

`starter_type` has **no direct edge** into `badges` in the structural equations. The "effect" of starter type on badges is entirely confounded --- it operates through the confounders `wealth` and `trainer_experience`, which drive both starter choice and badge outcomes through other variables.

This is a key pedagogical point of the textbook: the naive association between starter type and badges is entirely spurious.

**Backdoor paths:**

1. `starter_type` $\leftarrow$ `wealth` $\to$ `dept_store_spending` $\to$ `badges`
2. `starter_type` $\leftarrow$ `wealth` $\to$ `exp_share_used` $\to$ `badges`
3. `starter_type` $\leftarrow$ `wealth` $\to$ `held_item_count` $\to$ `badges`
4. `starter_type` $\leftarrow$ `trainer_experience` $\to$ `strategy_score` $\to$ `badges`
5. `starter_type` $\leftarrow$ `trainer_experience` $\to$ `team_level_avg` $\to$ `badges`
6. `starter_type` $\leftarrow$ `trainer_experience` $\to$ `type_diversity` $\to$ `badges`
7. `starter_type` $\leftarrow$ `trainer_experience` $\to$ `tm_count` $\to$ `badges`

**True causal effect:** Zero (no direct or mediated path exists from `starter_type` to `badges`). After proper adjustment, the estimated effect should be approximately zero.

---

## C.6 DAG Reading Guide

### How to Use the DAG to Determine What to Control For

1. **Identify your treatment ($T$) and outcome ($Y$).**
2. **List all paths** between $T$ and $Y$ (both directed and non-directed).
3. **Classify each path:**
   - **Causal path (directed, $T \to \cdots \to Y$):** Leave open. Do *not* control for variables on this path (doing so blocks the effect you want to estimate).
   - **Backdoor path ($T \leftarrow \cdots \to Y$ or $T \leftarrow \cdots \leftarrow \cdots \to Y$):** Must be blocked. Find a variable on the path to condition on.
   - **Paths through colliders ($T \to C \leftarrow Y$ or similar):** Already blocked by default. Do *not* condition on the collider or its descendants.
4. **Check your proposed adjustment set $\mathbf{Z}$:**
   - Does it block all backdoor paths? (Necessary.)
   - Does it avoid blocking any causal paths? (Necessary.)
   - Does it avoid opening any collider paths? (Necessary.)
   - Does it satisfy positivity? (For every stratum of $\mathbf{Z}$, there must be both treated and control units.)

### Common Mistakes in This DAG

| Mistake | Why It Is Wrong |
|:---|:---|
| Controlling for `strategy_score` when estimating `exp_share_used` $\to$ `badges` | `strategy_score` is a descendant of `trainer_experience` and lies on a causal pathway. While not a direct mediator of `exp_share_used` $\to$ `badges`, conditioning on it partially blocks information from `trainer_experience`, and if `trainer_experience` is omitted from the adjustment set, bias remains. |
| Controlling for `badges` as a covariate | Never condition on the outcome variable. |
| Controlling for `elite_four_attempted` | This is a direct descendant (child) of `badges`. Conditioning on it is conditioning on a post-treatment variable. |
| Controlling for `starter_type` when estimating `wealth` $\to$ `badges` | `starter_type` is a collider on the path `wealth` $\to$ `starter_type` $\leftarrow$ `trainer_experience`. Conditioning on it opens a spurious path between `wealth` and `trainer_experience`. |
| Ignoring latent variables | `patience`, `natural_talent`, and `dedication` are confounders for several relationships. If these are unavailable (as in a real observational study), some causal effects are not identifiable from observed data alone without additional assumptions. |

### Reconstructing the DAG Programmatically

The following Python snippet recreates the DAG using `pgmpy` and `graphviz`:

```python
import graphviz

dot = graphviz.Digraph("kanto_dag", format="png")
dot.attr(rankdir="LR", fontsize="10")

# Latent nodes (dashed)
for node in ["patience", "natural_talent", "dedication"]:
    dot.node(node, style="dashed", color="gray")

# Exogenous observed
for node in ["hometown", "trainer_experience"]:
    dot.node(node, shape="box")

# All edges (subset shown; full list in C.3)
edges = [
    ("hometown", "wealth"),
    ("patience", "strategy_score"),
    ("patience", "safari_zone_visits"),
    ("patience", "fishing_attempts"),
    ("patience", "type_diversity"),
    ("patience", "team_happiness_avg"),
    ("natural_talent", "strategy_score"),
    ("natural_talent", "team_avg_iv_total"),
    ("natural_talent", "elite_four_wins"),
    ("dedication", "play_hours"),
    ("dedication", "potions_purchased"),
    ("dedication", "tm_count"),
    ("dedication", "cave_training"),
    ("dedication", "team_happiness_avg"),
    ("dedication", "team_level_avg"),
    ("trainer_experience", "strategy_score"),
    ("trainer_experience", "starter_type"),
    ("trainer_experience", "team_size"),
    ("trainer_experience", "team_level_avg"),
    ("trainer_experience", "type_diversity"),
    ("trainer_experience", "play_hours"),
    ("trainer_experience", "cave_training"),
    ("trainer_experience", "tm_count"),
    ("trainer_experience", "exp_share_used"),
    ("trainer_experience", "traded_pokemon_count"),
    ("trainer_experience", "total_battles_won"),
    ("wealth", "starter_type"),
    ("wealth", "dept_store_spending"),
    ("wealth", "exp_share_used"),
    ("wealth", "held_item_count"),
    ("wealth", "rare_candy_used"),
    ("play_hours", "dept_store_spending"),
    ("play_hours", "potions_purchased"),
    ("play_hours", "revives_used"),
    ("play_hours", "gym_pokemon_center_visits"),
    ("play_hours", "team_avg_ev_total"),
    ("play_hours", "total_pokemon_caught"),
    ("play_hours", "hall_of_fame_time"),
    ("cave_training", "team_avg_ev_total"),
    ("tm_count", "held_item_count"),
    ("safari_zone_visits", "total_pokemon_caught"),
    ("team_level_avg", "team_level_max"),
    ("team_happiness_avg", "team_friendship_max"),
    ("total_pokemon_caught", "pokedex_completion"),
    # Into badges
    ("strategy_score", "badges"),
    ("team_level_avg", "badges"),
    ("type_diversity", "badges"),
    ("tm_count", "badges"),
    ("dept_store_spending", "badges"),
    ("exp_share_used", "badges"),
    ("held_item_count", "badges"),
    # Post-badge
    ("badges", "elite_four_attempted"),
    ("elite_four_attempted", "elite_four_wins"),
    ("strategy_score", "elite_four_wins"),
    ("team_level_avg", "elite_four_wins"),
    ("type_diversity", "elite_four_wins"),
    ("tm_count", "elite_four_wins"),
    ("elite_four_wins", "champion_defeated"),
    ("champion_defeated", "hall_of_fame_time"),
    ("strategy_score", "total_battles_won"),
    ("team_level_avg", "total_battles_won"),
]

for src, dst in edges:
    dot.edge(src, dst)

dot.render("kanto_full_dag", view=True)
```

---

> **Professor Oak's Final Note**
>
> "This DAG is both a map and a warning. It shows you which paths lead to truth and which lead to bias. In the real world, you never get to see the true DAG --- you must reason about it, defend it, and test its implications. But here, in this textbook, I am giving you the answer key. Use it wisely."

---

*Next: Appendix D --- Glossary: The Causal Pokedex*
