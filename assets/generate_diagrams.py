"""Generate the DAG diagrams referenced in the textbook chapters.

These are causal directed acyclic graphs used as figures in Chapters 1, 3, 4, 5,
6, 7, and 8. Each diagram is rendered with matplotlib (no graphviz dependency)
using the Kanto color palette.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

OUT = Path(__file__).parent / "diagrams"
OUT.mkdir(exist_ok=True)

KANTO_RED   = "#EE1515"
KANTO_BLUE  = "#3B4CCA"
KANTO_YEL   = "#FFD733"
KANTO_GREEN = "#4DAD5B"
KANTO_GRAY  = "#888888"
KANTO_BG    = "#FAFAF5"


def setup_axes(ax, xlim=(-5, 5), ylim=(-3, 3), title=""):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(KANTO_BG)
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold", pad=12, color="#222")


def draw_node(ax, x, y, label, color=KANTO_BLUE, latent=False, radius=0.55):
    edge = "#222" if not latent else KANTO_GRAY
    ls = "solid" if not latent else "dashed"
    facecolor = "white" if latent else color
    textcolor = "#222" if latent else "white"
    circle = Circle(
        (x, y), radius,
        facecolor=facecolor, edgecolor=edge, linewidth=2.2,
        linestyle=ls, zorder=3,
    )
    ax.add_patch(circle)
    ax.text(x, y, label, ha="center", va="center",
            fontsize=10, fontweight="bold", color=textcolor, zorder=4)


def draw_arrow(ax, p1, p2, color="#222", style="-|>", lw=1.8, dashed=False, label=None, label_pos=0.5, curve=0.0):
    ls = "dashed" if dashed else "solid"
    connectionstyle = "arc3" if curve == 0 else f"arc3,rad={curve}"
    arrow = FancyArrowPatch(
        p1, p2, arrowstyle=style, color=color, lw=lw,
        linestyle=ls, mutation_scale=14,
        shrinkA=18, shrinkB=18,
        connectionstyle=connectionstyle, zorder=2,
    )
    ax.add_patch(arrow)
    if label:
        mx = p1[0] + label_pos * (p2[0] - p1[0])
        my = p1[1] + label_pos * (p2[1] - p1[1]) + 0.18
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=9, color="#444", style="italic")


def save(name: str, fig) -> None:
    p = OUT / name
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor=KANTO_BG)
    plt.close(fig)
    print(f"  {p.name}")


# ---------------------------------------------------------------------------
# DAG 1: Confounding triangle (Ch 1, 3)
# ---------------------------------------------------------------------------
def dag_confounding():
    fig, ax = plt.subplots(figsize=(7, 4))
    setup_axes(ax, xlim=(-4.5, 4.5), ylim=(-2, 2.4), title="A Confounder")
    draw_node(ax, -3.0, -1.0, "D\nTreat", color=KANTO_RED)
    draw_node(ax,  3.0, -1.0, "Y\nOutcome", color=KANTO_BLUE)
    draw_node(ax,  0.0,  1.4, "Z\nConfounder", color=KANTO_YEL)
    draw_arrow(ax, (0.0, 1.4), (-3.0, -1.0))
    draw_arrow(ax, (0.0, 1.4), (3.0, -1.0))
    draw_arrow(ax, (-3.0, -1.0), (3.0, -1.0))
    ax.text(0, -1.7, "spurious + causal paths both contribute",
            ha="center", fontsize=9, style="italic", color="#666")
    save("dag_confounding.png", fig)


# ---------------------------------------------------------------------------
# DAG 2: Fork / Chain / Collider (Ch 3)
# ---------------------------------------------------------------------------
def dag_three_structures():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.patch.set_facecolor(KANTO_BG)

    # Fork: X <- Z -> Y
    ax = axes[0]
    setup_axes(ax, xlim=(-3, 3), ylim=(-2, 2.2), title="Fork  (Common Cause)")
    draw_node(ax, -2, -0.8, "X", color=KANTO_RED)
    draw_node(ax,  2, -0.8, "Y", color=KANTO_BLUE)
    draw_node(ax,  0,  1.2, "Z", color=KANTO_YEL)
    draw_arrow(ax, (0, 1.2), (-2, -0.8))
    draw_arrow(ax, (0, 1.2), (2, -0.8))
    ax.text(0, -1.6, "X ⊥ Y | Z   (condition to block)",
            ha="center", fontsize=9, style="italic", color="#444")

    # Chain: X -> Z -> Y
    ax = axes[1]
    setup_axes(ax, xlim=(-3, 3), ylim=(-2, 2.2), title="Chain  (Mediation)")
    draw_node(ax, -2, 0, "X", color=KANTO_RED)
    draw_node(ax,  0, 0, "Z", color=KANTO_YEL)
    draw_node(ax,  2, 0, "Y", color=KANTO_BLUE)
    draw_arrow(ax, (-2, 0), (0, 0))
    draw_arrow(ax, (0, 0), (2, 0))
    ax.text(0, -1.6, "X ⊥ Y | Z   (conditioning kills the effect!)",
            ha="center", fontsize=9, style="italic", color="#444")

    # Collider: X -> Z <- Y
    ax = axes[2]
    setup_axes(ax, xlim=(-3, 3), ylim=(-2, 2.2), title="Collider")
    draw_node(ax, -2, 1.2, "X", color=KANTO_RED)
    draw_node(ax,  2, 1.2, "Y", color=KANTO_BLUE)
    draw_node(ax,  0, -0.8, "Z", color=KANTO_YEL)
    draw_arrow(ax, (-2, 1.2), (0, -0.8))
    draw_arrow(ax, (2, 1.2), (0, -0.8))
    ax.text(0, -1.6, "X ⊥ Y     (do NOT condition on Z!)",
            ha="center", fontsize=9, style="italic", color="#444")

    fig.suptitle("The Three Atomic DAG Structures",
                 fontsize=15, fontweight="bold", y=1.02)
    save("dag_three_structures.png", fig)


# ---------------------------------------------------------------------------
# DAG 3: Backdoor criterion / Kanto trainer DAG (Ch 3)
# ---------------------------------------------------------------------------
def dag_backdoor():
    fig, ax = plt.subplots(figsize=(9, 6))
    setup_axes(ax, xlim=(-5, 5), ylim=(-3.2, 3.5), title="The Kanto Trainer DAG")

    nodes = {
        "Wealth":    (-3.5,  2.2),
        "Experience":(-1.0,  2.7),
        "Strategy":  ( 1.5,  2.0),
        "Items":     (-3.5,  0.2),
        "Cave":      (-1.0,  0.5),
        "Team":      ( 2.0, -0.2),
        "Badges":    ( 0.5, -2.2),
    }
    colors = {
        "Wealth":     KANTO_YEL,
        "Experience": KANTO_YEL,
        "Strategy":   KANTO_YEL,
        "Items":      KANTO_RED,
        "Cave":       KANTO_RED,
        "Team":       KANTO_GREEN,
        "Badges":     KANTO_BLUE,
    }
    for name, (x, y) in nodes.items():
        draw_node(ax, x, y, name, color=colors[name], radius=0.65)

    edges = [
        ("Wealth",     "Items"),
        ("Wealth",     "Cave"),
        ("Experience", "Strategy"),
        ("Experience", "Cave"),
        ("Strategy",   "Badges"),
        ("Items",      "Team"),
        ("Cave",       "Team"),
        ("Team",       "Badges"),
        ("Strategy",   "Team"),
    ]
    for src, dst in edges:
        draw_arrow(ax, nodes[src], nodes[dst])

    save("dag_kanto_trainer.png", fig)


# ---------------------------------------------------------------------------
# DAG 4: Bad control / Post-treatment bias (Ch 5)
# ---------------------------------------------------------------------------
def dag_bad_control():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    setup_axes(ax, xlim=(-4, 4), ylim=(-2.2, 2.4), title="Bad Control: Post-Treatment Variable")

    draw_node(ax, -2.8, 0, "Exp\nShare", color=KANTO_RED)
    draw_node(ax,  0.0, 0, "Team\nLevel", color=KANTO_GRAY, latent=False)
    draw_node(ax,  2.8, 0, "Badges", color=KANTO_BLUE)

    draw_arrow(ax, (-2.8, 0), (0, 0))
    draw_arrow(ax, (0, 0), (2.8, 0))
    draw_arrow(ax, (-2.8, 0), (2.8, 0), curve=-0.4)

    ax.text(0, -1.6,
            "Controlling for Team Level blocks the causal pathway → BAD",
            ha="center", fontsize=10, style="italic", color="#a02020")
    save("dag_bad_control.png", fig)


# ---------------------------------------------------------------------------
# DAG 5: IV (Ch 6)
# ---------------------------------------------------------------------------
def dag_iv():
    fig, ax = plt.subplots(figsize=(8, 5))
    setup_axes(ax, xlim=(-4, 4.5), ylim=(-2.5, 2.5), title="Instrumental Variable")

    draw_node(ax, -3.0, 0, "Z\nLottery", color=KANTO_YEL)
    draw_node(ax,  0.0, 0, "D\nSafari", color=KANTO_RED)
    draw_node(ax,  3.0, 0, "Y\nWins", color=KANTO_BLUE)
    draw_node(ax,  1.5, 1.7, "U\nPatience", color="#FFFFFF", latent=True)

    draw_arrow(ax, (-3.0, 0), (0.0, 0))
    draw_arrow(ax, (0.0, 0), (3.0, 0))
    draw_arrow(ax, (1.5, 1.7), (0.0, 0))
    draw_arrow(ax, (1.5, 1.7), (3.0, 0))

    ax.text(0, -1.6, "Z affects Y only through D  (exclusion restriction)",
            ha="center", fontsize=10, style="italic", color="#444")
    ax.text(1.5, 2.4, "unobserved", ha="center", fontsize=8, color="#666", style="italic")
    save("dag_iv.png", fig)


# ---------------------------------------------------------------------------
# DAG 6: RDD (Ch 6)
# ---------------------------------------------------------------------------
def dag_rdd():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_facecolor(KANTO_BG)

    np.random.seed(151)
    n = 200
    x = np.random.uniform(150, 280, n)
    treat = (x >= 220).astype(float)
    y = 30 + 0.15 * (x - 220) + 12 * treat + np.random.normal(0, 4, n)

    ax.scatter(x[treat == 0], y[treat == 0], alpha=0.55, color=KANTO_BLUE, s=22, label="Below threshold")
    ax.scatter(x[treat == 1], y[treat == 1], alpha=0.55, color=KANTO_RED, s=22, label="Above threshold")
    ax.axvline(220, color="#222", linestyle="--", linewidth=2, label="Cutoff (happiness=220)")

    # local linear fits
    for mask, color in [(treat == 0, KANTO_BLUE), (treat == 1, KANTO_RED)]:
        xs = np.linspace(x[mask].min(), x[mask].max(), 100)
        coeffs = np.polyfit(x[mask], y[mask], 1)
        ax.plot(xs, np.polyval(coeffs, xs), color=color, linewidth=2.5)

    ax.set_xlabel("Happiness score (running variable)", fontsize=11)
    ax.set_ylabel("Battle performance (outcome)", fontsize=11)
    ax.set_title("Regression Discontinuity at the Evolution Threshold",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    save("rdd_evolution.png", fig)


# ---------------------------------------------------------------------------
# DAG 7: DiD parallel trends (Ch 7)
# ---------------------------------------------------------------------------
def did_parallel_trends():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_facecolor(KANTO_BG)

    t = np.arange(1, 13)
    treat_period = 6
    control = 50 + 1.2 * t
    treated_pre = 45 + 1.2 * t
    treated_post = 45 + 1.2 * t + np.where(t > treat_period, 8 + 0.5 * (t - treat_period), 0)

    ax.plot(t, control, "o-", color=KANTO_BLUE, lw=2.5, label="Cerulean (control)")
    ax.plot(t[t <= treat_period], treated_post[t <= treat_period],
            "o-", color=KANTO_RED, lw=2.5, label="Saffron (treated)")
    ax.plot(t[t >= treat_period], treated_post[t >= treat_period],
            "o-", color=KANTO_RED, lw=2.5)
    ax.plot(t[t >= treat_period], treated_pre[t >= treat_period],
            "o--", color=KANTO_RED, lw=1.8, alpha=0.5, label="Counterfactual")

    ax.axvline(treat_period, color="#222", linestyle=":", linewidth=2)
    ax.text(treat_period + 0.2, 80, "Shadow Surge\nreleased", fontsize=9, color="#444")

    ax.set_xlabel("Time period (months)", fontsize=11)
    ax.set_ylabel("Average win rate (%)", fontsize=11)
    ax.set_title("Difference-in-Differences: Saffron vs Cerulean",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    save("did_parallel_trends.png", fig)


# ---------------------------------------------------------------------------
# DAG 8: Mediation (Ch 8)
# ---------------------------------------------------------------------------
def dag_mediation():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    setup_axes(ax, xlim=(-4, 4), ylim=(-2, 2.2), title="Mediation: Total = Direct + Indirect")

    draw_node(ax, -2.8, -0.5, "T\nItem use", color=KANTO_RED)
    draw_node(ax,  0.0,  1.2, "M\nHealth", color=KANTO_YEL)
    draw_node(ax,  2.8, -0.5, "Y\nWin", color=KANTO_BLUE)

    draw_arrow(ax, (-2.8, -0.5), (0.0, 1.2), label="a")
    draw_arrow(ax, (0.0, 1.2), (2.8, -0.5), label="b")
    draw_arrow(ax, (-2.8, -0.5), (2.8, -0.5), label="c'  (NDE)", curve=-0.3)

    save("dag_mediation.png", fig)


def main():
    print("Generating chapter DAG diagrams")
    print("=" * 60)
    dag_confounding()
    dag_three_structures()
    dag_backdoor()
    dag_bad_control()
    dag_iv()
    dag_rdd()
    did_parallel_trends()
    dag_mediation()
    print("=" * 60)
    print(f"Done. {len(list(OUT.glob('*.png')))} diagrams in {OUT}")


if __name__ == "__main__":
    main()
