"""
theme.py
Full color system: a light content area (same blue/teal brand accents as
before) paired with a dark-navy + gold sidebar, inspired by premium HR/SaaS
dashboards.
"""

# --- Content area (light) ---
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
SECONDARY = "#14B8A6"
SECONDARY_HOVER = "#0D9488"
ACCENT = "#8B5CF6"

BG = "#F3F5FA"
CARD = "#FFFFFF"
BORDER = "#E4E8F1"

TEXT_DARK = "#101B45"
TEXT_BODY = "#374162"
TEXT_MUTED = "#7C86A8"

SUCCESS = "#10B981"
SUCCESS_BG = "#ECFDF5"
WARNING = "#F4B400"
WARNING_BG = "#FFF8E1"
DANGER = "#EF4444"
DANGER_BG = "#FEF2F2"

# --- Sidebar (dark navy + gold) ---
SIDEBAR_BG = "#101B45"
SIDEBAR_BG_LIGHT = "#182657"
SIDEBAR_TEXT = "#E7EAF6"
SIDEBAR_MUTED = "#8891BD"
GOLD = "#F4B400"
GOLD_HOVER = "#DFA300"


def score_color(score):
    """Returns (color, bg) for a score, matching the green/blue/gold/red convention."""
    if score >= 80:
        return SUCCESS, SUCCESS_BG
    elif score >= 60:
        return PRIMARY, "#EFF6FF"
    elif score >= 40:
        return WARNING, WARNING_BG
    else:
        return DANGER, DANGER_BG
