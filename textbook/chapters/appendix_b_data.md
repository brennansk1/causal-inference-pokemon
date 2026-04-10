# Appendix B: Python Environment & Data Guide

---

*"Every great trainer needs the right gear before heading out," Nurse Joy says, organizing a shelf of healing supplies. "You wouldn't leave the Pokemon Center without Potions. Don't start coding without setting up your environment."*

---

## B.1 Installation & Environment Setup

### Option 1: pip (simplest)

```bash
# Create a virtual environment (recommended)
python -m venv kanto-env
source kanto-env/bin/activate    # macOS / Linux
kanto-env\Scripts\activate       # Windows

# Install the textbook package and all dependencies
pip install -e ".[all]"
```

### Option 2: conda (recommended for scientific computing)

```bash
# Create the environment from the provided YAML file
conda env create -f environment.yml

# Activate
conda activate kanto-causal

# Install the textbook package in development mode
pip install -e .
```

### Option 3: Manual installation

If you prefer to install packages individually:

```bash
pip install numpy pandas scipy statsmodels matplotlib seaborn
pip install scikit-learn econml dowhy causal-learn
pip install linearmodels pgmpy graphviz
pip install ipywidgets plotly jupyterlab
pip install -e .   # install kanto_utils from the repo root
```

### Verifying your installation

Run this quick check in Python:

```python
import kanto_utils
print(kanto_utils.__version__)   # Should print "1.0.0"

df = kanto_utils.load_trainers()
print(df.shape)                  # Should print (2000, 42)
print("Setup complete!")
```

---

## B.2 Package Reference

The following table lists every Python package used in this textbook, grouped by purpose.

### Core Scientific Stack

| Package | Version | Purpose |
|:---|:---:|:---|
| **numpy** | >= 1.24 | Array operations, random number generation, linear algebra. The backbone of all numerical computation. |
| **pandas** | >= 2.0 | DataFrames for tabular data. Every dataset in this textbook is loaded as a pandas DataFrame. |
| **scipy** | >= 1.10 | Statistical functions (`scipy.stats`), optimization (`scipy.optimize`), kernel density estimation. Used for hypothesis tests, distribution fitting, and bandwidth selection. |

### Statistical Modeling

| Package | Version | Purpose |
|:---|:---:|:---|
| **statsmodels** | >= 0.14 | OLS, logistic regression, IV/2SLS, robust standard errors, formula interface (`smf.ols`). Workhorse for Chapters 4--9. |
| **linearmodels** | >= 5.0 | Panel data models, two-way fixed effects (TWFE), instrumental variables with panel structure. Used in Chapters 7 and 9. |
| **scikit-learn** | >= 1.3 | Machine learning models: random forests, cross-validation, train/test splitting. Used primarily in Chapter 10 for causal forests and DML. |

### Causal Inference Libraries

| Package | Version | Purpose |
|:---|:---:|:---|
| **econml** | >= 0.15 | Microsoft's library for heterogeneous treatment effects: causal forests, DML, doubly robust learners, CATE estimation. Central to Chapter 10. |
| **dowhy** | >= 0.11 | End-to-end causal inference workflow: model specification, identification, estimation, refutation. Integrates with econml estimators. |
| **causal-learn** | >= 0.1 | Causal discovery algorithms (PC, GES, FCI). Used in Chapter 12 for learning DAG structure from data. |
| **pgmpy** | >= 0.1 | Probabilistic graphical models: Bayesian networks, DAG manipulation, d-separation queries. Used in Chapter 3 for DAG operations. |

### Visualization

| Package | Version | Purpose |
|:---|:---:|:---|
| **matplotlib** | >= 3.7 | Base plotting library. All static figures use matplotlib via the Kanto theme (`apply_kanto_theme()`). |
| **seaborn** | >= 0.13 | Statistical plots: kernel density, violin plots, heatmaps. Built on matplotlib. |
| **graphviz** | >= 0.20 | DAG rendering. Requires the Graphviz system package (`brew install graphviz` on macOS, `sudo apt install graphviz` on Linux). |
| **plotly** | >= 5.18 | Interactive plots for sensitivity analysis dashboards, 3D treatment effect surfaces. Used selectively. |

### Interactive & Notebook Tools

| Package | Version | Purpose |
|:---|:---:|:---|
| **ipywidgets** | >= 8.0 | Interactive sliders and widgets for the confounder adjustment demo, RDD bandwidth explorer, and power analysis tool. |
| **jupyterlab** | >= 4.0 | Notebook environment. All textbook code is designed to run in Jupyter notebooks. |

---

## B.3 The `kanto_utils` Package

The `kanto_utils` package is the textbook's companion library. It provides data loaders, themed plotting functions, causal estimators, interactive widgets, and narrative callout boxes. All functions are importable from the top-level namespace.

### Module Overview

| Module | Description |
|:---|:---|
| `kanto_utils.data_loader` | Functions to load each of the 11 datasets from `data/raw/`. |
| `kanto_utils.plotting` | Kanto-themed matplotlib styling, specialized causal inference plots (love plots, RDD plots, DiD plots). |
| `kanto_utils.causal` | Estimator functions: difference in means, randomization inference, propensity scores, IPW, doubly robust, Wald/2SLS, sharp RDD, DiD. |
| `kanto_utils.widgets` | Interactive Jupyter widgets for exploring causal concepts. |
| `kanto_utils.narrative` | Callout box helpers for themed narrative elements (Professor Oak, Blue, Nurse Joy, Gym Leaders). |

### Data Loaders

```python
from kanto_utils import (
    load_trainers,          # kanto_trainers.csv -- 2,000 rows, 42 cols
    load_battles,           # kanto_battles.csv -- 50,000 rows, 28 cols
    load_cities_panel,      # kanto_cities_panel.csv -- city x month panel
    load_protein_rct,       # pewter_protein_rct.csv -- RCT data
    load_ss_anne,           # ss_anne_passengers.csv -- matching data
    load_safari_lottery,    # safari_zone_lottery.csv -- IV data
    load_happiness,         # happiness_evolution.csv -- RDD data
    load_shadow_surge,      # shadow_surge_staggered.csv -- staggered DiD
    load_elite_four,        # elite_four_panel.csv -- dynamic treatment
    load_double_battles,    # double_battles.csv -- interference
    load_johto,             # johto_transportability.csv -- external validity
)
```

Each loader returns a `pd.DataFrame`. All functions accept `**kwargs` which are passed through to `pd.read_csv()`.

### Plotting Utilities

```python
from kanto_utils import (
    type_color,          # Get the hex color for a Pokemon type string
    type_colors_dict,    # Full dict: {"Fire": "#F08030", "Water": "#6890F0", ...}
    apply_kanto_theme,   # Apply the textbook's matplotlib rcParams theme
    badge_stamp,         # Add a badge icon to a figure (for "badge earned" moments)
    pokemon_scatter,     # Themed scatter plot with type-colored markers
    love_plot,           # Covariate balance (love) plot for matching chapters
    did_plot,            # Difference-in-differences parallel trends visualization
    rdd_plot,            # Regression discontinuity plot with cutoff line
)
```

**Applying the theme.** Call `apply_kanto_theme()` once at the top of each notebook to set consistent fonts, colors, and grid styling:

```python
import matplotlib.pyplot as plt
from kanto_utils import apply_kanto_theme

apply_kanto_theme()
# All subsequent plots will use the Kanto theme
```

### Causal Estimators

```python
from kanto_utils import (
    difference_in_means,       # Simple ATE via treated - control means
    randomization_inference,   # Fisher's exact p-value via permutation
    propensity_score,          # Fit propensity score model, return scores
    ipw_estimate,              # Inverse probability weighting ATE
    doubly_robust,             # AIPW / doubly robust estimator
    wald_estimator,            # Wald (IV) estimator for a single instrument
    two_stage_ls,              # Two-stage least squares
    sharp_rdd,                 # Local linear regression for sharp RDD
    did_estimate,              # Difference-in-differences estimator
    balance_table,             # Covariate balance table (pre/post matching)
)
```

### Interactive Widgets

```python
from kanto_utils import (
    confounder_slider,         # Adjust confounding strength and see bias change
    rdd_bandwidth_slider,      # Explore bandwidth sensitivity in RDD
    power_analysis_widget,     # Interactive sample size / power calculator
    starter_selector,          # Choose a starter and see causal implications
)
```

### Narrative Callout Boxes

```python
from kanto_utils import (
    oak_says,           # Professor Oak explanation box
    blue_says,          # Blue's (often wrong) claim
    nurse_joy_says,     # Nurse Joy's practical advice
    gym_leader_says,    # Gym Leader challenge/insight
    badge_earned,       # Badge milestone marker
    blues_mistake,      # Highlight a common causal reasoning error
)
```

Usage example:

```python
oak_says("Ignorability means that, conditional on the covariates, "
         "treatment assignment is as good as random.")
```

---

## B.4 Data Generation

### Philosophy

All datasets in this textbook are **synthetically generated** from known structural equations. This design choice is deliberate: because we control the data-generating process (DGP), we know the *true* causal effects. Students can check their estimates against the ground truth, building intuition for when methods work and when they fail.

### Regenerating the Data

All datasets are generated by `data/dgp/structural_equations.py` using a single random number generator seeded with **seed = 151** (one for each original Pokemon):

```python
import numpy as np
RNG = np.random.default_rng(151)
```

To regenerate all datasets from scratch:

```bash
cd data/dgp
python generate_all.py
```

This will overwrite the CSV files in `data/raw/`. Because the seed is fixed, the output is deterministic --- every student gets identical data.

### Why seed = 151?

There are 151 Pokemon in the original Kanto Pokedex. The seed is a nod to Mew, #151, the hidden Pokemon that contains the DNA of all others. Similarly, our single seed contains the DNA of all 11 datasets.

---

## B.5 Dataset Quick Reference

| Dataset | File | Rows | Cols | Chapter(s) | Key Variables |
|:---|:---|:---:|:---:|:---:|:---|
| Kanto Trainers | `kanto_trainers.csv` | 2,000 | 42 | 1--6, 10 | `trainer_id`, `starter_type`, `badges`, `strategy_score`, `wealth`, `trainer_experience`, `exp_share_used` |
| Kanto Battles | `kanto_battles.csv` | 50,000 | 28 | 1, 4 | `battle_id`, `trainer_id`, `battle_type`, `attacker_level`, `defender_level`, `won` |
| Kanto Cities Panel | `kanto_cities_panel.csv` | ~240 | ~15 | 9 | `city`, `month`, `gym_present`, `population`, `pokemon_center_visits` |
| Pewter Protein RCT | `pewter_protein_rct.csv` | ~500 | ~12 | 4, 7 | `assigned_treatment`, `took_protein`, `battle_performance`, `pokemon_id` |
| S.S. Anne Passengers | `ss_anne_passengers.csv` | ~1,500 | ~20 | 5, 6 | `passenger_id`, `ticket_class`, `survived`, `trainer_level`, `pokemon_count` |
| Safari Zone Lottery | `safari_zone_lottery.csv` | ~2,000 | ~15 | 7 | `won_lottery`, `visited_safari`, `rare_pokemon_owned`, `battle_score` |
| Happiness Evolution | `happiness_evolution.csv` | ~3,000 | ~12 | 8 | `pokemon_id`, `happiness`, `evolved`, `battle_stats_post` |
| Shadow Surge | `shadow_surge_staggered.csv` | ~600 | ~15 | 9 | `city`, `period`, `treatment_start`, `shadow_pokemon_count`, `trainer_activity` |
| Elite Four Panel | `elite_four_panel.csv` | ~800 | ~18 | 11 | `challenger_id`, `attempt`, `preparation`, `team_composition`, `outcome` |
| Double Battles | `double_battles.csv` | ~5,000 | ~20 | 11 | `battle_id`, `partner_type`, `interference`, `outcome`, `partner_outcome` |
| Johto Trainers | `johto_transportability.csv` | ~1,000 | ~30 | 12 | `trainer_id`, `region`, `starter_type`, `badges`, `strategy_score` |

---

## B.6 Codebook Conventions

Throughout this textbook, data dictionaries follow consistent conventions:

### Variable Naming

- **Snake case:** All variable names use `lower_snake_case` (e.g., `team_level_avg`, `dept_store_spending`).
- **Suffixes:**
  - `_id` --- unique identifier (not for analysis; for merging only)
  - `_avg` --- mean value across a group
  - `_max` --- maximum value across a group
  - `_count` --- count of occurrences
  - `_used` --- binary indicator (0/1) of whether something was used
  - `_score` --- continuous index, typically 0--100

### Variable Types

| Type Label | Meaning | Example |
|:---|:---|:---|
| **continuous** | Numeric, can take any real value in a range | `team_level_avg` (5--100) |
| **count** | Non-negative integer | `safari_zone_visits` (0--30) |
| **binary** | 0/1 indicator | `exp_share_used`, `cave_training` |
| **ordinal** | Ordered integer categories | `wealth` (1--5) |
| **categorical** | Unordered string categories | `starter_type`, `hometown` |
| **latent** | Not directly observable; included for DGP transparency | `patience`, `natural_talent`, `dedication` |

### Missing Values

Missing values are encoded as `NaN` in pandas. The only dataset with structural missingness is `kanto_trainers.csv`, where `hall_of_fame_time` is `NaN` for trainers who did not defeat the Champion (this is by design, not data error).

---

## B.7 Common Code Patterns

### Loading Data and Applying the Theme

```python
import pandas as pd
import matplotlib.pyplot as plt
from kanto_utils import load_trainers, apply_kanto_theme

# Apply the visual theme
apply_kanto_theme()

# Load the main dataset
df = load_trainers()
print(f"Dataset: {df.shape[0]} trainers, {df.shape[1]} variables")
df.head()
```

### Quick Exploratory Summary

```python
# Summary statistics for key variables
df[["badges", "strategy_score", "wealth", "trainer_experience"]].describe()
```

### Creating a Themed Scatter Plot

```python
from kanto_utils import pokemon_scatter

pokemon_scatter(
    df,
    x="strategy_score",
    y="badges",
    hue="starter_type",
    title="Strategy Score vs. Badges by Starter Type",
)
plt.tight_layout()
plt.show()
```

### Running a Quick Causal Estimate

```python
from kanto_utils import difference_in_means, ipw_estimate

# Naive difference in means
naive = difference_in_means(df, treatment="exp_share_used", outcome="badges")
print(f"Naive DiM: {naive['estimate']:.3f} (SE: {naive['se']:.3f})")

# IPW estimate adjusting for confounders
ipw = ipw_estimate(
    df,
    treatment="exp_share_used",
    outcome="badges",
    covariates=["wealth", "trainer_experience", "strategy_score"],
)
print(f"IPW ATE:   {ipw['estimate']:.3f} (SE: {ipw['se']:.3f})")
```

### Using Narrative Callouts in Notebooks

```python
from kanto_utils import oak_says, blues_mistake

oak_says(
    "The IPW estimate is closer to the true effect because it "
    "adjusts for the confounders that drive both Exp. Share usage "
    "and badge outcomes."
)

blues_mistake(
    "Blue compared Exp. Share users to non-users without adjustment. "
    "Wealthier trainers are more likely to buy Exp. Share AND earn "
    "more badges due to other advantages."
)
```

---

> **Nurse Joy's Reminder:** "If something breaks, check your Python version (>= 3.10), make sure you installed in the right environment, and remember that `graphviz` needs both the Python package *and* the system binary. Come back to the Pokemon Center --- I mean, this appendix --- anytime."

---

*Next: Appendix C --- The Full Kanto Causal DAG*
