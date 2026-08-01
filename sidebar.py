"""
sidebar.py
Custom sidebar built entirely from native st.button widgets styled via
CSS (see styles.py). Deliberately avoids iframe-based components (like
streamlit-option-menu) because their internal DOM lives in a separate
document that our page CSS cannot reach - that was causing invisible
nav text and a broken sidebar background.
"""

import streamlit as st

APPLICANT_PAGES = [
    {"key": "dashboard", "label": "Dashboard", "icon": ":material/speed:"},
]

HR_PAGES = [
    {"key": "hr_dashboard", "label": "Dashboard", "icon": ":material/dashboard:"},
    {"key": "hr_bulk", "label": "Bulk Screening", "icon": ":material/folder_open:"},
    {"key": "hr_analytics", "label": "Analytics", "icon": ":material/bar_chart:"},
    {"key": "hr_email", "label": "Email Center", "icon": ":material/mail:"},
]


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 18px 0 20px 0;">
                <div class="brand-avatar">HL</div>
                <div style="font-size:20px; font-weight:800; color:white;">HireLens</div>
                <div class="sidebar-subtext" style="margin-top:2px;">
                    Smart Resume Screening
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Portal switch ---
        col1, col2 = st.columns(2)
        applicant_active = st.session_state.portal == "applicant"
        hr_active = st.session_state.portal == "hr"

        applicant_clicked = col1.button(
            "Applicant", key="switch_applicant", width='stretch',
            type="primary" if applicant_active else "secondary",
            icon=":material/badge:",
        )
        hr_clicked = col2.button(
            "HR Portal", key="switch_hr", width='stretch',
            type="primary" if hr_active else "secondary",
            icon=":material/apartment:",
        )

        if applicant_clicked and not applicant_active:
            st.session_state.portal = "applicant"
            st.session_state.page = APPLICANT_PAGES[0]["key"]
            st.rerun()
        if hr_clicked and not hr_active:
            st.session_state.portal = "hr"
            st.session_state.page = HR_PAGES[0]["key"]
            st.rerun()

        st.markdown("<hr/>", unsafe_allow_html=True)

        # --- Page nav for the active portal ---
        pages = APPLICANT_PAGES if st.session_state.portal == "applicant" else HR_PAGES
        for p in pages:
            is_active = st.session_state.page == p["key"]
            clicked = st.button(
                p["label"], key=f"nav_{p['key']}", width='stretch',
                type="primary" if is_active else "secondary",
                icon=p["icon"],
            )
            if clicked and not is_active:
                st.session_state.page = p["key"]
                st.rerun()

        st.markdown(
            """
            <div class="sidebar-footer">HireLens · v1.0</div>
            """,
            unsafe_allow_html=True,
        )
