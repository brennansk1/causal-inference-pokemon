"""
Pokemon-themed plotting utilities for Causal Inference: A Pokemon Approach.

Provides colour palettes, a custom matplotlib style, and high-level plotting
functions tailored to causal inference visualisations with a Kanto flavour.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as patheffects
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Pokemon type colours (official-ish hex values for all 18 types)
# ---------------------------------------------------------------------------

_TYPE_COLORS: Dict[str, str] = {
    "normal":   "#A8A77A",
    "fire":     "#EE8130",
    "water":    "#6390F0",
    "electric": "#F7D02C",
    "grass":    "#7AC74C",
    "ice":      "#96D9D6",
    "fighting": "#C22E28",
    "poison":   "#A33EA1",
    "ground":   "#E2BF65",
    "flying":   "#A98FF3",
    "psychic":  "#F95587",
    "bug":      "#A6B91A",
    "rock":     "#B6A136",
    "ghost":    "#735797",
    "dragon":   "#6F35FC",
    "dark":     "#705746",
    "steel":    "#B7B7CE",
    "fairy":    "#D685AD",
}


def type_color(pokemon_type: str) -> str:
    """Return the hex colour string for a Pokemon type.

    Parameters
    ----------
    pokemon_type : str
        One of the 18 Pokemon types (case-insensitive).

    Returns
    -------
    str
        Hex colour code, e.g. ``'#EE8130'`` for fire.

    Raises
    ------
    KeyError
        If the type is not recognised.
    """
    key = pokemon_type.strip().lower()
    if key not in _TYPE_COLORS:
        raise KeyError(
            f"Unknown Pokemon type '{pokemon_type}'. "
            f"Valid types: {', '.join(sorted(_TYPE_COLORS))}"
        )
    return _TYPE_COLORS[key]


def type_colors_dict() -> Dict[str, str]:
    """Return the full mapping of Pokemon types to hex colours.

    Returns
    -------
    dict
        ``{type_name: hex_color}`` for all 18 types.
    """
    return dict(_TYPE_COLORS)


# ---------------------------------------------------------------------------
# Matplotlib style
# ---------------------------------------------------------------------------

def _find_style_file() -> Path:
    """Locate ``kanto_theme.mplstyle`` in the project assets."""
    anchor = Path(__file__).resolve().parent
    for parent in (anchor, *anchor.parents):
        candidate = parent / "assets" / "kanto_theme.mplstyle"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Could not find assets/kanto_theme.mplstyle. "
        "Make sure you are running from inside the textbook repository."
    )


def apply_kanto_theme() -> None:
    """Activate the Kanto matplotlib style globally.

    Loads ``assets/kanto_theme.mplstyle`` so that every subsequent plot
    uses the textbook's visual identity.  Safe to call multiple times.
    """
    style_path = _find_style_file()
    plt.style.use(str(style_path))


# ---------------------------------------------------------------------------
# Badge stamp
# ---------------------------------------------------------------------------

# Canonical Kanto badge names and their colours
_BADGE_STYLES: Dict[str, str] = {
    "boulder":  "#B6A136",
    "cascade":  "#6390F0",
    "thunder":  "#F7D02C",
    "rainbow":  "#7AC74C",
    "soul":     "#F95587",
    "marsh":    "#A33EA1",
    "volcano":  "#EE8130",
    "earth":    "#E2BF65",
}


def badge_stamp(badge_name: str, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Draw a *Badge Earned!* stamp on a matplotlib axes.

    Places a semi-transparent circular stamp in the upper-right corner of the
    axes, styled after the named Kanto gym badge.

    Parameters
    ----------
    badge_name : str
        Name of a Kanto gym badge (e.g. ``'boulder'``, ``'cascade'``).
        Case-insensitive.
    ax : matplotlib.axes.Axes, optional
        Target axes.  Uses ``plt.gca()`` if *None*.

    Returns
    -------
    matplotlib.axes.Axes
        The axes with the badge stamp drawn.
    """
    if ax is None:
        ax = plt.gca()

    key = badge_name.strip().lower()
    color = _BADGE_STYLES.get(key, "#888888")
    label = f"{badge_name.title()} Badge"

    # Draw a circle in axes-fraction coordinates via a custom transform
    from matplotlib.patches import Circle
    stamp = Circle(
        (0.88, 0.88),
        radius=0.08,
        transform=ax.transAxes,
        facecolor=color,
        edgecolor="white",
        linewidth=2.5,
        alpha=0.75,
        zorder=10,
    )
    ax.add_patch(stamp)

    # Add text inside the stamp
    txt = ax.text(
        0.88, 0.88,
        label,
        transform=ax.transAxes,
        fontsize=6,
        fontweight="bold",
        color="white",
        ha="center",
        va="center",
        zorder=11,
    )
    txt.set_path_effects([
        patheffects.withStroke(linewidth=1.5, foreground=color),
    ])

    return ax


# ---------------------------------------------------------------------------
# Pokemon scatter plot
# ---------------------------------------------------------------------------

def pokemon_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    hue: Optional[str] = None,
    sprites: bool = False,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """Create a styled scatter plot with optional Pokemon-type colouring.

    Parameters
    ----------
    df : pd.DataFrame
        Data source.
    x, y : str
        Column names for the horizontal and vertical axes.
    hue : str, optional
        Column used to colour the points.  If the column values are Pokemon
        types, official type colours are used automatically.
    sprites : bool, default False
        If *True* and a ``'sprite_path'`` column exists, renders tiny
        Pokemon sprites instead of scatter dots (requires Pillow).
    ax : matplotlib.axes.Axes, optional
        Target axes.  A new figure is created when *None*.
    **kwargs
        Extra keyword arguments forwarded to ``ax.scatter``.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        _, ax = plt.subplots()

    scatter_kw = dict(s=60, alpha=0.75, edgecolors="white", linewidths=0.5)
    scatter_kw.update(kwargs)

    if hue is not None and hue in df.columns:
        groups = df[hue].unique()
        # Check if hue values look like Pokemon types
        is_type_hue = all(g.lower() in _TYPE_COLORS for g in groups if isinstance(g, str))

        for group in sorted(groups, key=str):
            mask = df[hue] == group
            color = (
                _TYPE_COLORS.get(str(group).lower(), None)
                if is_type_hue
                else None
            )
            kw = dict(scatter_kw)
            if color is not None:
                kw["color"] = color

            if sprites and "sprite_path" in df.columns:
                _draw_sprites(df.loc[mask], x, y, ax)
            else:
                ax.scatter(df.loc[mask, x], df.loc[mask, y], label=str(group), **kw)

        ax.legend(title=hue, frameon=True, framealpha=0.9)
    else:
        if sprites and "sprite_path" in df.columns:
            _draw_sprites(df, x, y, ax)
        else:
            ax.scatter(df[x], df[y], **scatter_kw)

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{y} vs {x}")
    return ax


def _draw_sprites(
    df: pd.DataFrame,
    x: str,
    y: str,
    ax: plt.Axes,
    zoom: float = 0.3,
) -> None:
    """Render Pokemon sprites at data coordinates (best-effort)."""
    try:
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        from PIL import Image
    except ImportError:
        # Fall back to normal scatter
        ax.scatter(df[x], df[y], s=40, alpha=0.7)
        return

    for _, row in df.iterrows():
        sprite_path = Path(row["sprite_path"])
        if not sprite_path.is_file():
            ax.plot(row[x], row[y], "o", ms=4, color="#888")
            continue
        img = Image.open(sprite_path).convert("RGBA")
        im = OffsetImage(np.array(img), zoom=zoom)
        ab = AnnotationBbox(im, (row[x], row[y]), frameon=False)
        ax.add_artist(ab)


# ---------------------------------------------------------------------------
# Love plot (covariate balance)
# ---------------------------------------------------------------------------

def love_plot(
    smd_before: Sequence[float],
    smd_after: Sequence[float],
    covariate_names: Sequence[str],
    threshold: float = 0.1,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Draw a Love plot showing covariate balance before and after matching.

    Parameters
    ----------
    smd_before : array-like
        Standardised mean differences before matching / weighting.
    smd_after : array-like
        Standardised mean differences after matching / weighting.
    covariate_names : array-like of str
        Labels for each covariate (same order as the SMD arrays).
    threshold : float, default 0.1
        Vertical dashed line indicating the acceptable balance threshold.
    ax : matplotlib.axes.Axes, optional
        Target axes.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, max(4, len(covariate_names) * 0.45)))

    smd_before = np.asarray(smd_before)
    smd_after = np.asarray(smd_after)
    n = len(covariate_names)
    y_pos = np.arange(n)

    ax.scatter(
        np.abs(smd_before), y_pos, marker="o", s=80, color="#EE1515",
        label="Before matching", zorder=3, edgecolors="white", linewidths=0.5,
    )
    ax.scatter(
        np.abs(smd_after), y_pos, marker="s", s=80, color="#3B4CCA",
        label="After matching", zorder=3, edgecolors="white", linewidths=0.5,
    )

    # Connect before -> after with lines
    for i in range(n):
        ax.plot(
            [np.abs(smd_before[i]), np.abs(smd_after[i])],
            [y_pos[i], y_pos[i]],
            color="#AAAAAA", linewidth=0.8, zorder=2,
        )

    # Threshold line
    ax.axvline(threshold, color="#FFD733", linestyle="--", linewidth=1.5,
               label=f"Threshold ({threshold})")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(covariate_names)
    ax.set_xlabel("Absolute Standardised Mean Difference")
    ax.set_title("Covariate Balance (Love Plot)")
    ax.legend(loc="lower right", frameon=True)
    ax.invert_yaxis()
    ax.set_xlim(left=0)
    return ax


# ---------------------------------------------------------------------------
# Difference-in-differences plot
# ---------------------------------------------------------------------------

def did_plot(
    df: pd.DataFrame,
    time_col: str,
    outcome_col: str,
    group_col: str,
    treatment_period: Union[int, float, str],
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Visualise a canonical difference-in-differences design.

    Plots group-level means over time with a vertical line at the treatment
    onset and an optional counterfactual trend for the treated group.

    Parameters
    ----------
    df : pd.DataFrame
        Panel / repeated cross-section data.
    time_col : str
        Column with the time variable.
    outcome_col : str
        Column with the outcome variable.
    group_col : str
        Binary column indicating treatment (1) and control (0) groups.
    treatment_period : int, float, or str
        Value in *time_col* at which treatment begins.
    ax : matplotlib.axes.Axes, optional
        Target axes.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        _, ax = plt.subplots()

    groups = sorted(df[group_col].unique())
    colors = {"treat": "#EE1515", "ctrl": "#3B4CCA"}

    for i, grp in enumerate(groups):
        grp_df = df[df[group_col] == grp]
        means = grp_df.groupby(time_col)[outcome_col].mean()
        role = "treat" if grp == max(groups) else "ctrl"
        label = "Treated" if role == "treat" else "Control"
        ax.plot(means.index, means.values, "o-", color=colors[role],
                label=label, linewidth=2, markersize=6)

        # Counterfactual for treated group
        if role == "treat":
            pre_mask = means.index < treatment_period
            if pre_mask.any():
                pre_times = means.index[pre_mask]
                pre_vals = means.values[pre_mask]
                if len(pre_times) >= 2:
                    # Linear extrapolation of the pre-treatment trend
                    coeffs = np.polyfit(
                        np.asarray(pre_times, dtype=float),
                        pre_vals, 1,
                    )
                    post_times = means.index[~pre_mask]
                    cf_vals = np.polyval(coeffs, np.asarray(post_times, dtype=float))
                    ax.plot(post_times, cf_vals, "--", color=colors[role],
                            alpha=0.5, linewidth=1.5, label="Counterfactual (treated)")

    ax.axvline(treatment_period, color="#FFD733", linestyle=":", linewidth=2,
               label="Treatment onset")
    ax.set_xlabel(time_col)
    ax.set_ylabel(outcome_col)
    ax.set_title("Difference-in-Differences")
    ax.legend(frameon=True)
    return ax


# ---------------------------------------------------------------------------
# Regression discontinuity plot
# ---------------------------------------------------------------------------

def rdd_plot(
    running_var: np.ndarray,
    outcome: np.ndarray,
    cutoff: float,
    bandwidth: Optional[float] = None,
    n_bins: int = 30,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Plot a regression-discontinuity design.

    Shows a binned scatter of outcomes against the running variable with
    separate local-linear fits on each side of the cutoff.

    Parameters
    ----------
    running_var : array-like
        The running / forcing variable.
    outcome : array-like
        The outcome variable.
    cutoff : float
        The RD cutoff value.
    bandwidth : float, optional
        If given, the plot is restricted to observations within this
        bandwidth of the cutoff.
    n_bins : int, default 30
        Number of bins for the binned scatter.
    ax : matplotlib.axes.Axes, optional
        Target axes.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        _, ax = plt.subplots()

    running_var = np.asarray(running_var, dtype=float)
    outcome = np.asarray(outcome, dtype=float)

    # Optional bandwidth restriction
    if bandwidth is not None:
        mask = np.abs(running_var - cutoff) <= bandwidth
        running_var = running_var[mask]
        outcome = outcome[mask]

    left_mask = running_var < cutoff
    right_mask = running_var >= cutoff

    # Binned scatter
    for mask, color, label in [
        (left_mask, "#3B4CCA", "Below cutoff"),
        (right_mask, "#EE1515", "Above cutoff"),
    ]:
        if not mask.any():
            continue
        rv_side = running_var[mask]
        oc_side = outcome[mask]

        # Create bins
        bins = np.linspace(rv_side.min(), rv_side.max(), n_bins // 2 + 1)
        bin_idx = np.digitize(rv_side, bins)
        bin_means_x = []
        bin_means_y = []
        for b in range(1, len(bins)):
            b_mask = bin_idx == b
            if b_mask.any():
                bin_means_x.append(rv_side[b_mask].mean())
                bin_means_y.append(oc_side[b_mask].mean())

        ax.scatter(bin_means_x, bin_means_y, color=color, s=50, zorder=3,
                   edgecolors="white", linewidths=0.5, label=label)

        # Local linear fit
        if len(rv_side) >= 2:
            coeffs = np.polyfit(rv_side, oc_side, 1)
            xs = np.linspace(rv_side.min(), rv_side.max(), 200)
            ax.plot(xs, np.polyval(coeffs, xs), color=color, linewidth=2)

    ax.axvline(cutoff, color="#FFD733", linestyle="--", linewidth=2,
               label=f"Cutoff = {cutoff}")
    ax.set_xlabel("Running variable")
    ax.set_ylabel("Outcome")
    ax.set_title("Regression Discontinuity Design")
    ax.legend(frameon=True)
    return ax
