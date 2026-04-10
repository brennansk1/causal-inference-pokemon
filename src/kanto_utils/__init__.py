"""
kanto_utils -- Helper utilities for *Causal Inference: A Pokemon Approach*.

This package provides data loaders, plotting helpers, causal inference
estimators, interactive widgets, and narrative callout boxes, all with a
Kanto Pokemon theme.
"""

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------
from .data_loader import (
    load_trainers,
    load_battles,
    load_cities_panel,
    load_protein_rct,
    load_ss_anne,
    load_safari_lottery,
    load_happiness,
    load_shadow_surge,
    load_elite_four,
    load_double_battles,
    load_johto,
)

# ---------------------------------------------------------------------------
# Plotting utilities
# ---------------------------------------------------------------------------
from .plotting import (
    type_color,
    type_colors_dict,
    apply_kanto_theme,
    badge_stamp,
    pokemon_scatter,
    love_plot,
    did_plot,
    rdd_plot,
)

# ---------------------------------------------------------------------------
# Causal inference estimators
# ---------------------------------------------------------------------------
from .causal import (
    difference_in_means,
    randomization_inference,
    propensity_score,
    ipw_estimate,
    doubly_robust,
    wald_estimator,
    two_stage_ls,
    sharp_rdd,
    did_estimate,
    balance_table,
)

# ---------------------------------------------------------------------------
# Interactive widgets
# ---------------------------------------------------------------------------
from .widgets import (
    confounder_slider,
    rdd_bandwidth_slider,
    power_analysis_widget,
    starter_selector,
)

# ---------------------------------------------------------------------------
# Narrative / callout helpers
# ---------------------------------------------------------------------------
from .narrative import (
    oak_says,
    blue_says,
    nurse_joy_says,
    gym_leader_says,
    badge_earned,
    blues_mistake,
)

# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------
__all__ = [
    # version
    "__version__",
    # data_loader
    "load_trainers",
    "load_battles",
    "load_cities_panel",
    "load_protein_rct",
    "load_ss_anne",
    "load_safari_lottery",
    "load_happiness",
    "load_shadow_surge",
    "load_elite_four",
    "load_double_battles",
    "load_johto",
    # plotting
    "type_color",
    "type_colors_dict",
    "apply_kanto_theme",
    "badge_stamp",
    "pokemon_scatter",
    "love_plot",
    "did_plot",
    "rdd_plot",
    # causal
    "difference_in_means",
    "randomization_inference",
    "propensity_score",
    "ipw_estimate",
    "doubly_robust",
    "wald_estimator",
    "two_stage_ls",
    "sharp_rdd",
    "did_estimate",
    "balance_table",
    # widgets
    "confounder_slider",
    "rdd_bandwidth_slider",
    "power_analysis_widget",
    "starter_selector",
    # narrative
    "oak_says",
    "blue_says",
    "nurse_joy_says",
    "gym_leader_says",
    "badge_earned",
    "blues_mistake",
]
