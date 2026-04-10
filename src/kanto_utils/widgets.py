"""
Interactive ipywidgets for Causal Inference: A Pokemon Approach.

These widgets are designed for use inside Jupyter notebooks, giving students
hands-on intuition for key causal inference ideas.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: safe widget import
# ---------------------------------------------------------------------------

def _check_widgets():
    """Import ipywidgets and IPython.display, raising a friendly error if
    unavailable."""
    try:
        import ipywidgets as widgets
        from IPython.display import display, clear_output
        return widgets, display, clear_output
    except ImportError:
        raise ImportError(
            "ipywidgets is required for interactive widgets.\n"
            "Install it with: pip install ipywidgets"
        )


# ---------------------------------------------------------------------------
# 1. Confounder slider
# ---------------------------------------------------------------------------

def confounder_slider(
    data: pd.DataFrame,
    treatment: str,
    outcome: str,
    confounder: str,
) -> None:
    """Interactive widget showing how controlling for a confounder changes the
    estimated treatment effect.

    A slider selects subsets of the data based on confounder quantile ranges.
    Two panels show:
      - **Left**: naive estimate (full data) vs. conditional estimate.
      - **Right**: scatter with confounder highlighted.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset with columns *treatment*, *outcome*, and *confounder*.
    treatment : str
        Name of the binary treatment column.
    outcome : str
        Name of the outcome column.
    confounder : str
        Name of the continuous confounder column.
    """
    widgets, display, clear_output = _check_widgets()

    q_min = float(data[confounder].min())
    q_max = float(data[confounder].max())

    slider = widgets.FloatRangeSlider(
        value=[q_min, q_max],
        min=q_min,
        max=q_max,
        step=(q_max - q_min) / 100,
        description="Confounder:",
        continuous_update=False,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="70%"),
    )

    output = widgets.Output()

    def _update(change):
        lo, hi = slider.value
        subset = data[(data[confounder] >= lo) & (data[confounder] <= hi)]

        with output:
            clear_output(wait=True)
            if subset[treatment].nunique() < 2 or len(subset) < 10:
                print("Too few observations in this range. Widen the slider.")
                return

            treated = subset[subset[treatment] == 1][outcome]
            control = subset[subset[treatment] == 0][outcome]
            cond_est = treated.mean() - control.mean()

            naive_treated = data[data[treatment] == 1][outcome]
            naive_control = data[data[treatment] == 0][outcome]
            naive_est = naive_treated.mean() - naive_control.mean()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

            # Left panel: bar chart of estimates
            bars = ax1.bar(
                ["Naive\n(full data)", f"Conditional\n({confounder} in [{lo:.1f}, {hi:.1f}])"],
                [naive_est, cond_est],
                color=["#EE1515", "#3B4CCA"],
                edgecolor="white",
                width=0.5,
            )
            ax1.set_ylabel(f"Estimated effect on {outcome}")
            ax1.set_title("Treatment Effect Estimates")
            for bar, val in zip(bars, [naive_est, cond_est]):
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{val:.3f}", ha="center", va="bottom", fontweight="bold")

            # Right panel: scatter coloured by treatment
            for t_val, color, label in [(0, "#3B4CCA", "Control"), (1, "#EE1515", "Treated")]:
                mask = data[treatment] == t_val
                ax2.scatter(
                    data.loc[mask, confounder], data.loc[mask, outcome],
                    alpha=0.3, s=20, color=color, label=label,
                )
            ax2.axvspan(lo, hi, color="#FFD733", alpha=0.2, label="Selected range")
            ax2.set_xlabel(confounder)
            ax2.set_ylabel(outcome)
            ax2.set_title("Data with confounder range highlighted")
            ax2.legend(frameon=True, fontsize=9)

            fig.tight_layout()
            plt.show()

    slider.observe(_update, names="value")
    _update(None)
    display(widgets.VBox([slider, output]))


# ---------------------------------------------------------------------------
# 2. RDD bandwidth slider
# ---------------------------------------------------------------------------

def rdd_bandwidth_slider(
    running_var: np.ndarray,
    outcome: np.ndarray,
    cutoff: float,
    bw_range: Optional[tuple] = None,
) -> None:
    """Interactive widget for exploring RDD bandwidth sensitivity.

    A slider controls the bandwidth around the cutoff.  The plot updates to
    show the local-linear fits and the estimated discontinuity.

    Parameters
    ----------
    running_var : array-like
        Running / forcing variable.
    outcome : array-like
        Outcome variable.
    cutoff : float
        RD cutoff.
    bw_range : tuple of (float, float), optional
        Min and max bandwidth for the slider.  Defaults to
        (0.5 * IQR, 2.0 * IQR) of the running variable.
    """
    widgets, display, clear_output = _check_widgets()
    from . import causal as _causal
    from . import plotting as _plot

    x = np.asarray(running_var, dtype=float)
    y = np.asarray(outcome, dtype=float)

    if bw_range is None:
        iqr = np.percentile(x, 75) - np.percentile(x, 25)
        bw_range = (max(0.1, 0.2 * iqr), 2.5 * iqr)

    slider = widgets.FloatSlider(
        value=np.mean(bw_range),
        min=bw_range[0],
        max=bw_range[1],
        step=(bw_range[1] - bw_range[0]) / 100,
        description="Bandwidth:",
        continuous_update=False,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="60%"),
    )

    output = widgets.Output()

    def _update(change):
        bw = slider.value
        with output:
            clear_output(wait=True)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

            # Left: RDD plot with current bandwidth
            try:
                _plot.rdd_plot(x, y, cutoff, bandwidth=bw, ax=ax1)
                ax1.set_title(f"RDD plot (bandwidth = {bw:.2f})")
            except ValueError as exc:
                ax1.text(0.5, 0.5, str(exc), transform=ax1.transAxes,
                         ha="center", va="center", fontsize=10, color="red")
                ax1.set_title("RDD plot")

            # Right: estimate + CI as a function of bandwidth
            bws = np.linspace(bw_range[0], bw_range[1], 40)
            estimates = []
            ci_lo = []
            ci_hi = []
            for b in bws:
                try:
                    res = _causal.sharp_rdd(x, y, cutoff, bandwidth=b)
                    estimates.append(res["estimate"])
                    ci_lo.append(res["ci_lower"])
                    ci_hi.append(res["ci_upper"])
                except (ValueError, np.linalg.LinAlgError):
                    estimates.append(np.nan)
                    ci_lo.append(np.nan)
                    ci_hi.append(np.nan)

            ax2.plot(bws, estimates, color="#EE1515", linewidth=2, label="Estimate")
            ax2.fill_between(bws, ci_lo, ci_hi, color="#EE1515", alpha=0.15,
                             label="95% CI")
            ax2.axvline(bw, color="#FFD733", linestyle="--", linewidth=2,
                        label=f"Current bw = {bw:.2f}")
            ax2.axhline(0, color="grey", linewidth=0.8, linestyle=":")
            ax2.set_xlabel("Bandwidth")
            ax2.set_ylabel("RD Estimate")
            ax2.set_title("Bandwidth Sensitivity")
            ax2.legend(frameon=True, fontsize=9)

            fig.tight_layout()
            plt.show()

    slider.observe(_update, names="value")
    _update(None)
    display(widgets.VBox([slider, output]))


# ---------------------------------------------------------------------------
# 3. Power analysis widget
# ---------------------------------------------------------------------------

def power_analysis_widget() -> None:
    """Interactive power analysis for a two-sample difference-in-means test.

    Sliders control sample size, effect size, significance level, and the
    allocation ratio.  The widget displays the statistical power and a
    power-curve plot.
    """
    widgets, display, clear_output = _check_widgets()
    from scipy import stats as sp_stats

    n_slider = widgets.IntSlider(
        value=100, min=10, max=2000, step=10,
        description="N per group:", style={"description_width": "initial"},
        layout=widgets.Layout(width="60%"),
    )
    es_slider = widgets.FloatSlider(
        value=0.3, min=0.01, max=2.0, step=0.01,
        description="Effect size (Cohen d):", style={"description_width": "initial"},
        layout=widgets.Layout(width="60%"),
    )
    alpha_slider = widgets.FloatSlider(
        value=0.05, min=0.001, max=0.20, step=0.001,
        description="Alpha:", style={"description_width": "initial"},
        layout=widgets.Layout(width="60%"),
    )

    output = widgets.Output()

    def _power(n, d, alpha):
        """Analytical power for a two-sample t-test (equal groups)."""
        se = np.sqrt(2 / n)  # assuming sigma=1 and equal n
        z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
        power = 1 - sp_stats.norm.cdf(z_alpha - d / se) + sp_stats.norm.cdf(-z_alpha - d / se)
        return power

    def _update(change):
        n = n_slider.value
        d = es_slider.value
        alpha = alpha_slider.value
        pwr = _power(n, d, alpha)

        with output:
            clear_output(wait=True)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

            # Left: power gauge
            ax1.barh(["Power"], [pwr], color="#3B4CCA" if pwr >= 0.8 else "#EE1515",
                     edgecolor="white", height=0.4)
            ax1.set_xlim(0, 1)
            ax1.axvline(0.8, color="#FFD733", linestyle="--", linewidth=2,
                        label="80% target")
            ax1.set_xlabel("Statistical Power")
            ax1.set_title(f"Power = {pwr:.3f}")
            ax1.legend(frameon=True)

            # Right: power curve over sample sizes
            ns = np.arange(10, 2010, 10)
            powers = [_power(nn, d, alpha) for nn in ns]
            ax2.plot(ns, powers, color="#3B4CCA", linewidth=2)
            ax2.axhline(0.8, color="#FFD733", linestyle="--", linewidth=1.5,
                        label="80%")
            ax2.axvline(n, color="#EE1515", linestyle=":", linewidth=2,
                        label=f"N = {n}")
            ax2.set_xlabel("Sample size per group")
            ax2.set_ylabel("Power")
            ax2.set_title(f"Power curve (d = {d:.2f}, alpha = {alpha:.3f})")
            ax2.set_ylim(0, 1.05)
            ax2.legend(frameon=True, fontsize=9)

            fig.tight_layout()
            plt.show()

    for s in (n_slider, es_slider, alpha_slider):
        s.observe(_update, names="value")
    _update(None)
    display(widgets.VBox([n_slider, es_slider, alpha_slider, output]))


# ---------------------------------------------------------------------------
# 4. Starter selector
# ---------------------------------------------------------------------------

_STARTERS = {
    "Bulbasaur": {
        "type": "Grass/Poison",
        "color": "#7AC74C",
        "number": 1,
        "description": (
            "Bulbasaur is the reliable choice -- like a well-specified linear "
            "model. Steady, dependable, and great in the early gyms (chapters)."
        ),
        "causal_analogy": (
            "If causal inference were a Pokemon journey, Bulbasaur represents "
            "randomised experiments: strong fundamentals that give you an "
            "advantage early on."
        ),
    },
    "Charmander": {
        "type": "Fire",
        "color": "#EE8130",
        "number": 4,
        "description": (
            "Charmander is the ambitious pick -- high risk, high reward. "
            "Struggles with early gyms but dominates later."
        ),
        "causal_analogy": (
            "Charmander is like instrumental variables: tricky to get right "
            "at first, but incredibly powerful once you master the technique."
        ),
    },
    "Squirtle": {
        "type": "Water",
        "color": "#6390F0",
        "number": 7,
        "description": (
            "Squirtle is the balanced choice -- solid defences and reliable "
            "throughout the game."
        ),
        "causal_analogy": (
            "Squirtle represents difference-in-differences: versatile, "
            "widely applicable, and trusted by practitioners everywhere."
        ),
    },
}


def starter_selector() -> None:
    """Fun 'choose your starter Pokemon' widget with causal inference analogies.

    Displays three starter buttons with descriptions linking each Pokemon to
    a causal inference concept.
    """
    widgets, display, clear_output = _check_widgets()
    from IPython.display import HTML

    output = widgets.Output()

    def _on_click(name):
        def handler(btn):
            info = _STARTERS[name]
            with output:
                clear_output(wait=True)
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 6)
                ax.set_aspect("equal")
                ax.axis("off")

                # Draw a card
                card = plt.Rectangle((0.5, 0.5), 9, 5, facecolor=info["color"],
                                     alpha=0.15, edgecolor=info["color"],
                                     linewidth=3, zorder=1)
                ax.add_patch(card)

                ax.text(5, 4.8, f"#{info['number']}  {name}", fontsize=18,
                        fontweight="bold", ha="center", va="center",
                        color=info["color"])
                ax.text(5, 4.0, f"Type: {info['type']}", fontsize=12,
                        ha="center", va="center", color="#555555")
                ax.text(5, 2.8, info["description"], fontsize=9,
                        ha="center", va="center", wrap=True, color="#333333",
                        style="italic")
                ax.text(5, 1.3, info["causal_analogy"], fontsize=9,
                        ha="center", va="center", wrap=True, color="#333333")

                fig.tight_layout()
                plt.show()

                display(HTML(
                    f"<p style='text-align:center; font-size:16px; "
                    f"color:{info['color']};'>"
                    f"<b>You chose {name}!</b> A fine choice, trainer.</p>"
                ))
        return handler

    buttons = []
    for name, info in _STARTERS.items():
        btn = widgets.Button(
            description=f"  {name}  ",
            button_style="",
            layout=widgets.Layout(width="180px", height="50px"),
            style={"button_color": info["color"], "font_weight": "bold"},
        )
        btn.on_click(_on_click(name))
        buttons.append(btn)

    header = widgets.HTML(
        "<h3 style='text-align:center;'>Professor Oak: Choose your starter Pokemon!</h3>"
        "<p style='text-align:center; color:#666;'>"
        "Each starter represents a different causal inference philosophy...</p>"
    )
    button_row = widgets.HBox(buttons, layout=widgets.Layout(
        justify_content="center", gap="20px",
    ))

    display(widgets.VBox([header, button_row, output]))
