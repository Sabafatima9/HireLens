"""
components.py
Reusable rendering helpers shared across pages: icon KPI cards, status
badges, and a Plotly circular gauge for the ATS score.
"""

import streamlit as st
import plotly.graph_objects as go

import theme


def kpi_card(col, title, value, color, icon):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{color};">
                <i class="bi bi-{icon}"></i>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_html(text, color, bg):
    return f'<span class="badge" style="color:{color};background:{bg};">{text}</span>'


def score_gauge(score, color, height=230):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 34, "color": theme.TEXT_DARK}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": theme.TEXT_MUTED},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": theme.CARD,
                "borderwidth": 0,
                "steps": [{"range": [0, 100], "color": theme.BORDER}],
            },
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor=theme.CARD,
        font={"family": "Inter, sans-serif"},
    )
    return fig
