"""
state_helpers.py
Initializes st.session_state keys once per session, so data survives
Streamlit's rerun-on-every-interaction behavior.
"""

import streamlit as st


def init_session_state():
    defaults = {
        "portal": "applicant",     # "applicant" or "hr" - drives the sidebar
        "page": "dashboard",       # current page key within that portal

        "candidates": [],          # HR bulk screening results
        "threshold": 50,
        "use_jd_hr": False,
        "jd_text_hr": "",
        "last_send_results": [],   # results of the most recent email send

        "last_result": None,       # applicant's most recent score result
        "last_result_mode": None,
        "user_history": [],        # session history of analyzed CVs

        "confirm_send_open": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def hr_stats():
    candidates = st.session_state.candidates
    total = len(candidates)
    passed = sum(1 for c in candidates if c["status"] == "Pass")
    rejected = sum(1 for c in candidates if c["status"] == "Reject")
    avg_score = round(sum(c["score"] for c in candidates) / total, 1) if total else 0
    emails_sent = sum(1 for r in st.session_state.last_send_results if r.get("success"))
    return {
        "total": total, "passed": passed, "rejected": rejected,
        "avg_score": avg_score, "emails_sent": emails_sent,
    }
