"""
styles.py
Injects custom CSS: bigger/friendlier typography, a dark-navy sidebar
with a gold active state (built from native buttons, not an iframe
component), rounded white cards for the content area, and forces a
light color-scheme so the app looks the same regardless of the user's
OS/browser dark-mode setting.
"""

import streamlit as st

import theme


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css');

        /* Force a light color-scheme so browser/OS dark mode can't invert
           form controls, scrollbars, etc. underneath our own theme. */
        :root {{ color-scheme: light; }}

        html, body, [class*="css"], .stApp {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 16px;
        }}

        .stApp {{ background-color: {theme.BG}; }}

        /* Hide default Streamlit chrome for a cleaner, branded app feel */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header[data-testid="stHeader"] {{ background: transparent; }}

        /* Bigger, bolder headings */
        h1 {{ font-size: 32px !important; font-weight: 800 !important; color: {theme.TEXT_DARK} !important; }}
        h2 {{ font-size: 24px !important; font-weight: 800 !important; color: {theme.TEXT_DARK} !important; }}
        h3, .stSubheader p {{ font-size: 20px !important; font-weight: 700 !important; color: {theme.TEXT_DARK} !important; }}
        [data-testid="stCaptionContainer"] p {{ font-size: 14px !important; color: {theme.TEXT_MUTED} !important; }}
        div[data-testid="stMarkdownContainer"] p {{ font-size: 16px; color: {theme.TEXT_BODY}; }}

        /* Card-style bordered containers (st.container(border=True)) */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 18px !important;
            border-color: {theme.BORDER} !important;
            background-color: {theme.CARD} !important;
        }}

        /* ---------------- Main-content buttons ---------------- */
        .stButton>button, .stDownloadButton>button {{
            border-radius: 10px;
            font-weight: 700;
            font-size: 15px;
            padding: 0.55rem 1.3rem;
        }}
        .stButton>button[kind="primary"] {{
            background-color: {theme.PRIMARY};
            border-color: {theme.PRIMARY};
            color: white !important;
        }}
        .stButton>button[kind="primary"]:hover {{
            background-color: {theme.PRIMARY_HOVER};
            border-color: {theme.PRIMARY_HOVER};
        }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background-color: {theme.CARD};
            border: 1px solid {theme.BORDER};
            border-radius: 16px;
            padding: 16px 20px;
        }}
        div[data-testid="stMetricValue"] {{ font-size: 30px !important; font-weight: 800 !important; }}

        /* File uploader dropzone */
        div[data-testid="stFileUploaderDropzone"] {{
            background-color: {theme.BG};
            border-radius: 16px;
            border: 2px dashed {theme.BORDER};
        }}

        /* Text areas / inputs */
        .stTextArea textarea, .stTextInput input, .stNumberInput input {{
            border-radius: 10px !important;
            font-size: 15px !important;
        }}

        /* ================= SIDEBAR ================= */
        /* Cover every possible nested wrapper Streamlit renders inside the
           sidebar - different versions use different inner testids, so we
           target several candidates defensively to avoid any white gaps. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
            background-color: {theme.SIDEBAR_BG} !important;
            min-height: 100vh;
        }}
        section[data-testid="stSidebar"] {{
            border-right: none;
            min-width: 280px !important;
        }}
        section[data-testid="stSidebar"] > div {{ padding-top: 0.5rem; }}
        section[data-testid="stSidebar"] hr {{
            border-color: {theme.SIDEBAR_BG_LIGHT};
            margin: 8px 0 16px 0;
        }}

        .sidebar-subtext {{ font-size: 12.5px; color: {theme.SIDEBAR_MUTED}; }}
        .sidebar-footer {{
            text-align: center; font-size: 11.5px; color: {theme.SIDEBAR_MUTED};
            padding: 18px 0 6px 0;
        }}

        /* Sidebar nav buttons - transparent/light-text by default, solid
           gold when active (type="primary" is set in sidebar.py). */
        section[data-testid="stSidebar"] .stButton>button {{
            text-align: left;
            justify-content: flex-start;
            font-size: 15px;
            font-weight: 600;
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 4px;
        }}
        section[data-testid="stSidebar"] .stButton>button[kind="secondary"] {{
            background-color: transparent !important;
            border: none !important;
            color: {theme.SIDEBAR_TEXT} !important;
        }}
        section[data-testid="stSidebar"] .stButton>button[kind="secondary"]:hover {{
            background-color: {theme.SIDEBAR_BG_LIGHT} !important;
            color: white !important;
        }}
        section[data-testid="stSidebar"] .stButton>button[kind="primary"] {{
            background-color: {theme.GOLD} !important;
            border: none !important;
            color: {theme.SIDEBAR_BG} !important;
        }}
        section[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover {{
            background-color: {theme.GOLD_HOVER} !important;
            color: {theme.SIDEBAR_BG} !important;
        }}

        /* Portal-switch pill background (the first columns row in the sidebar) */
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:first-of-type {{
            background-color: {theme.SIDEBAR_BG_LIGHT};
            border-radius: 12px;
            padding: 4px;
        }}
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:first-of-type .stButton>button {{
            font-size: 13px;
            padding: 8px 6px;
            justify-content: center;
            text-align: center;
        }}

        /* ---------------- Generic helper classes ---------------- */
        .kpi-card {{
            background: {theme.CARD};
            border: 1px solid {theme.BORDER};
            border-radius: 16px;
            padding: 18px 22px;
            height: 100%;
        }}
        .kpi-icon {{
            width: 38px; height: 38px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; color: white; margin-bottom: 10px;
        }}
        .kpi-value {{ font-size: 28px; font-weight: 800; color: {theme.TEXT_DARK}; line-height: 1.2; }}
        .kpi-label {{ font-size: 13px; color: {theme.TEXT_MUTED}; margin-top: 2px; }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
        }}

        .hero-card {{
            background: linear-gradient(135deg, {theme.SIDEBAR_BG} 0%, #1E2C63 100%);
            border-radius: 20px;
            padding: 28px 32px;
            color: white;
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
        }}
        .hero-card::after {{
            content: "";
            position: absolute;
            top: -40px; right: -40px;
            width: 160px; height: 160px;
            border-radius: 50%;
            background: {theme.GOLD}22;
        }}
        .hero-title {{ color: white !important; margin: 0; font-size: 26px; font-weight: 800; position: relative; }}
        .hero-subtitle {{ color: #C9D2F0 !important; margin: 8px 0 0 0; font-size: 15px; position: relative; }}

        .brand-avatar {{
            width: 56px; height: 56px; border-radius: 50%;
            background: {theme.GOLD};
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 800; color: {theme.SIDEBAR_BG};
            margin: 0 auto 10px auto;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
