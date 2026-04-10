"""
Callout box helpers for consistent narrative styling in notebooks.

Each function renders styled HTML via ``IPython.display`` to create
character-themed callout boxes that make the textbook's narrative voice
consistent and visually distinctive.
"""

from __future__ import annotations

from typing import Optional


# ---------------------------------------------------------------------------
# Shared rendering
# ---------------------------------------------------------------------------

def _display_html(html: str) -> None:
    """Render an HTML string in a Jupyter notebook."""
    try:
        from IPython.display import display, HTML
        display(HTML(html))
    except ImportError:
        # Fallback for non-IPython environments
        print(html)


def _callout_box(
    title: str,
    body: str,
    border_color: str,
    bg_color: str,
    emoji: str,
    title_color: Optional[str] = None,
) -> str:
    """Build a styled HTML callout box.

    Parameters
    ----------
    title : str
        Header text.
    body : str
        Body text (may contain HTML).
    border_color : str
        CSS colour for the left border accent.
    bg_color : str
        Background colour of the box.
    emoji : str
        Emoji/icon prepended to the title.
    title_color : str, optional
        Colour for the title text.  Defaults to *border_color*.

    Returns
    -------
    str
        Complete HTML string.
    """
    if title_color is None:
        title_color = border_color

    return (
        f'<div style="'
        f"margin: 1em 0; "
        f"padding: 1em 1.4em; "
        f"border-left: 5px solid {border_color}; "
        f"background-color: {bg_color}; "
        f"border-radius: 6px; "
        f"font-family: 'Segoe UI', Roboto, sans-serif; "
        f"line-height: 1.6; "
        f'">'
        f'<p style="margin:0 0 0.4em 0; font-weight:700; font-size:1.05em; '
        f'color:{title_color};">{emoji} {title}</p>'
        f'<p style="margin:0; color:#333;">{body}</p>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Character callouts
# ---------------------------------------------------------------------------

def oak_says(text: str) -> None:
    """Display a Professor Oak explanation callout.

    Use this for key conceptual explanations and definitions.

    Parameters
    ----------
    text : str
        The explanation text (plain text or HTML).
    """
    html = _callout_box(
        title="Professor Oak says",
        body=text,
        border_color="#4DAD5B",
        bg_color="#F0F9F0",
        emoji="\U0001F9D1\u200D\U0001F3EB",  # teacher emoji
    )
    _display_html(html)


def blue_says(text: str) -> None:
    """Display a Rival Blue causal-fallacy callout.

    Use this to highlight common causal reasoning mistakes that students
    (like Blue) tend to make.

    Parameters
    ----------
    text : str
        Blue's fallacious claim or reasoning.
    """
    html = _callout_box(
        title="Blue says",
        body=text,
        border_color="#3B4CCA",
        bg_color="#EEF0FF",
        emoji="\U0001F4A2",  # anger emoji
    )
    _display_html(html)


def nurse_joy_says(text: str) -> None:
    """Display a Nurse Joy hint / tip callout.

    Use this for practical tips, coding advice, and encouragement.

    Parameters
    ----------
    text : str
        The hint or tip text.
    """
    html = _callout_box(
        title="Nurse Joy says",
        body=text,
        border_color="#FF69B4",
        bg_color="#FFF0F6",
        emoji="\U0001F496",  # sparkling heart emoji
    )
    _display_html(html)


def gym_leader_says(name: str, text: str) -> None:
    """Display a callout from a named Gym Leader.

    Use this for chapter-specific insights from the corresponding Gym
    Leader character.

    Parameters
    ----------
    name : str
        Gym Leader name (e.g. ``'Brock'``, ``'Misty'``).
    text : str
        The Gym Leader's advice or insight.
    """
    # Gym leader colour palette
    _GYM_COLORS = {
        "brock":    ("#B6A136", "#FAF6E6"),
        "misty":    ("#6390F0", "#EBF2FF"),
        "lt. surge": ("#F7D02C", "#FFFDE6"),
        "erika":    ("#7AC74C", "#F0F9F0"),
        "koga":     ("#A33EA1", "#F8F0F8"),
        "sabrina":  ("#F95587", "#FFF0F4"),
        "blaine":   ("#EE8130", "#FFF3EB"),
        "giovanni": ("#E2BF65", "#FAF6E6"),
    }

    key = name.strip().lower()
    border_color, bg_color = _GYM_COLORS.get(key, ("#888888", "#F5F5F5"))

    html = _callout_box(
        title=f"Gym Leader {name.title()} says",
        body=text,
        border_color=border_color,
        bg_color=bg_color,
        emoji="\U0001F396\uFE0F",  # medal emoji
    )
    _display_html(html)


# ---------------------------------------------------------------------------
# Badge earned celebration
# ---------------------------------------------------------------------------

def badge_earned(badge_name: str, chapter: int) -> None:
    """Display a celebratory badge-earned banner.

    Show this at the end of a chapter when the student has completed
    all exercises.

    Parameters
    ----------
    badge_name : str
        Name of the badge earned (e.g. ``'Boulder'``).
    chapter : int
        Chapter number.
    """
    _BADGE_COLORS = {
        "boulder":  "#B6A136",
        "cascade":  "#6390F0",
        "thunder":  "#F7D02C",
        "rainbow":  "#7AC74C",
        "soul":     "#F95587",
        "marsh":    "#A33EA1",
        "volcano":  "#EE8130",
        "earth":    "#E2BF65",
    }

    key = badge_name.strip().lower()
    color = _BADGE_COLORS.get(key, "#888888")

    html = (
        f'<div style="'
        f"margin: 1.5em 0; "
        f"padding: 1.5em 2em; "
        f"text-align: center; "
        f"background: linear-gradient(135deg, {color}22, {color}44); "
        f"border: 3px solid {color}; "
        f"border-radius: 12px; "
        f"font-family: 'Segoe UI', Roboto, sans-serif; "
        f'">'
        f'<p style="font-size:2em; margin:0;">\U0001F3C6</p>'
        f'<p style="font-size:1.4em; font-weight:800; color:{color}; margin:0.3em 0;">'
        f"Congratulations!</p>"
        f'<p style="font-size:1.15em; color:#333; margin:0.2em 0;">'
        f"You earned the <b>{badge_name.title()} Badge</b>!</p>"
        f'<p style="font-size:0.95em; color:#666; margin:0.5em 0 0 0;">'
        f"Chapter {chapter} complete. Your causal inference journey continues...</p>"
        f"</div>"
    )
    _display_html(html)


# ---------------------------------------------------------------------------
# Blue's mistake: side-by-side comparison
# ---------------------------------------------------------------------------

def blues_mistake(claim: str, reality: str) -> None:
    """Display a side-by-side box contrasting Blue's causal mistake with
    the correct reasoning.

    Parameters
    ----------
    claim : str
        Blue's incorrect causal claim.
    reality : str
        The correct causal reasoning.
    """
    html = (
        '<div style="'
        "margin: 1em 0; "
        "display: flex; "
        "gap: 1em; "
        "font-family: 'Segoe UI', Roboto, sans-serif; "
        "line-height: 1.6; "
        '">'
        # Left column: Blue's mistake
        '<div style="'
        "flex: 1; "
        "padding: 1em 1.2em; "
        "border-left: 5px solid #EE1515; "
        "background-color: #FFF0F0; "
        "border-radius: 6px; "
        '">'
        '<p style="margin:0 0 0.4em 0; font-weight:700; font-size:1.05em; '
        'color:#EE1515;">\U0000274C Blue\'s Claim</p>'
        f'<p style="margin:0; color:#333; font-style:italic;">'
        f'"{claim}"</p>'
        "</div>"
        # Right column: correct reasoning
        '<div style="'
        "flex: 1; "
        "padding: 1em 1.2em; "
        "border-left: 5px solid #4DAD5B; "
        "background-color: #F0F9F0; "
        "border-radius: 6px; "
        '">'
        '<p style="margin:0 0 0.4em 0; font-weight:700; font-size:1.05em; '
        'color:#4DAD5B;">\U00002705 Correct Reasoning</p>'
        f'<p style="margin:0; color:#333;">{reality}</p>'
        "</div>"
        "</div>"
    )
    _display_html(html)
