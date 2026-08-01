"""
app.py
Entry point for HireLens. Run with:  streamlit run app.py
Uses a fully custom sidebar (streamlit-option-menu) instead of the
default st.navigation chrome, for complete control over the look.
"""

import streamlit as st

st.set_page_config(
    page_title="HireLens - ATS Resume Screening",
    page_icon=":material/badge:",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles import inject_css
import state_helpers

inject_css()
state_helpers.init_session_state()

from sidebar import render_sidebar
from pages_app.applicant_dashboard import render as applicant_dashboard
from pages_app.hr_dashboard import render as hr_dashboard
from pages_app.hr_bulk_screening import render as hr_bulk_screening
from pages_app.hr_analytics import render as hr_analytics
from pages_app.hr_email_center import render as hr_email_center

render_sidebar()

PAGE_RENDERERS = {
    "dashboard": applicant_dashboard,
    "hr_dashboard": hr_dashboard,
    "hr_bulk": hr_bulk_screening,
    "hr_analytics": hr_analytics,
    "hr_email": hr_email_center,
}

PAGE_RENDERERS[st.session_state.page]()
