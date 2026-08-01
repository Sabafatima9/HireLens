"""
pages_app/hr_analytics.py
HR Portal - Recruitment Analytics: score distribution histogram and a
pass/reject breakdown, built from the current session's candidates.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

import theme


def render():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.subheader("Recruitment Analytics", anchor=False)
        st.caption("Insights from the current screening session")
    with col2:
        st.button("Refresh", width='stretch', key="analytics_refresh", icon=":material/refresh:")

    candidates = st.session_state.candidates
    if not candidates:
        st.info("No data yet — process a batch of CVs in **Bulk Screening** first.", icon=":material/info:")
        return

    df = pd.DataFrame(candidates)

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("**ATS Score Distribution**")
            fig1 = px.histogram(
                df, x="score", nbins=10, range_x=[0, 100],
                color_discrete_sequence=[theme.PRIMARY],
            )
            fig1.update_layout(
                bargap=0.1, height=350, paper_bgcolor=theme.CARD, plot_bgcolor=theme.CARD,
                xaxis_title="Score (%)", yaxis_title="Candidates",
                font={"family": "Inter, sans-serif", "color": theme.TEXT_BODY},
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig1, width='stretch')

    with col2:
        with st.container(border=True):
            st.markdown("**Shortlisted vs Rejected**")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            color_map = {"Pass": theme.SUCCESS, "Reject": theme.DANGER}
            fig2 = px.pie(
                status_counts, names="status", values="count",
                color="status", color_discrete_map=color_map, hole=0.45,
            )
            fig2.update_layout(
                height=350, paper_bgcolor=theme.CARD,
                font={"family": "Inter, sans-serif", "color": theme.TEXT_BODY},
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig2, width='stretch')
