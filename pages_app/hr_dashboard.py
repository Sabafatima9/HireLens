"""
pages_app/hr_dashboard.py
HR Portal - Dashboard: executive KPI overview of the current screening session.
"""

import streamlit as st

import theme
import state_helpers
from components import kpi_card


def render():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.subheader("HR Dashboard", anchor=False)
        st.caption("Overview of your current screening session")
    with col2:
        st.button("Refresh", width='stretch', icon=":material/refresh:")

    stats = state_helpers.hr_stats()

    if stats["total"] == 0:
        st.info("No CVs processed yet — head to **Bulk Screening** to get started.", icon=":material/info:")
        return

    cards = [
        ("Total Applicants", stats["total"], theme.PRIMARY, "people-fill"),
        ("Shortlisted", stats["passed"], theme.SUCCESS, "check-circle-fill"),
        ("Rejected", stats["rejected"], theme.DANGER, "x-circle-fill"),
        ("Average ATS Score", f"{stats['avg_score']}%", theme.ACCENT, "graph-up"),
        ("Rejection Emails Sent", stats["emails_sent"], theme.SECONDARY, "envelope-check-fill"),
    ]

    cols = st.columns(3)
    for i, (title, value, color, icon) in enumerate(cards):
        kpi_card(cols[i % 3], title, value, color, icon)
        if i % 3 == 2:
            st.write("")
