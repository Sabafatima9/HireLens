"""
pages_app/applicant_dashboard.py
Applicant Portal - Dashboard: upload a CV, optionally match against a
Job Description, see a circular ATS score gauge + breakdown, plus a
running session history.
"""

import os
import tempfile
import datetime

import streamlit as st

import theme
import cv_parser
import ats_scorer
from components import score_gauge, badge_html


def render():
    st.markdown(
        """
        <div class="hero-card">
            <h2 class="hero-title">Welcome back</h2>
            <p class="hero-subtitle">
                Upload your CV to see how it scores against real ATS criteria.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.subheader("Upload Resume", anchor=False)
        st.caption("PDF or DOCX, one file at a time")

        uploaded = st.file_uploader("Upload your CV", type=["pdf", "docx"], label_visibility="collapsed")
        use_jd = st.toggle("Match against a Job Description", key="applicant_jd_toggle")

        jd_text = ""
        if use_jd:
            jd_text = st.text_area("Paste the Job Description", height=140, key="applicant_jd_text")

        analyze = st.button("Analyze CV", type="primary", icon=":material/search_insights:")

    if analyze:
        _run_analysis(uploaded, use_jd, jd_text)

    if st.session_state.last_result:
        _render_result(st.session_state.last_result, st.session_state.last_result_mode)

    _render_history()


def _run_analysis(uploaded, use_jd, jd_text):
    if not uploaded:
        st.warning("Please upload a CV first.")
        return

    suffix = os.path.splitext(uploaded.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner("Reading and scoring your resume..."):
            cv_text = cv_parser.extract_text(tmp_path)
    except Exception as e:
        st.error(f"Error reading CV: {e}")
        return
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    if not cv_text.strip():
        st.error("Couldn't extract any text from this file. It may be a scanned image.")
        return

    name = cv_parser.extract_name(cv_text, fallback_filename=uploaded.name)

    if use_jd:
        if not jd_text.strip():
            st.warning("Please paste a job description, or turn the toggle off.")
            return
        result = ats_scorer.score_against_jd(cv_text, jd_text)
        mode_label = "JD Match"
    else:
        result = ats_scorer.score_general(cv_text)
        mode_label = "General Health"

    st.session_state.last_result = result
    st.session_state.last_result_mode = mode_label
    st.session_state.user_history.insert(0, {
        "name": name,
        "score": result["score"],
        "mode": mode_label,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
    })

    st.toast(f"Analysis complete — {result['score']}% score", icon=":material/task_alt:")
    if result["score"] >= 80:
        st.balloons()


def _render_result(result, mode_label):
    with st.container(border=True):
        title = "ATS Match Result" if mode_label == "JD Match" else "CV Health Check"
        st.subheader(title, anchor=False)

        color, bg = theme.score_color(result["score"])
        col1, col2 = st.columns([1, 2])

        with col1:
            st.plotly_chart(score_gauge(result["score"], color), width='stretch')

        with col2:
            if mode_label == "JD Match":
                st.write(
                    f"Matched **{len(result['matched'])}** of **{result['total_keywords']}** "
                    f"key terms from the job description."
                )
                if result["missing"]:
                    st.markdown("**Missing keywords worth adding:**")
                    st.markdown(
                        " ".join(badge_html(kw, theme.DANGER, theme.DANGER_BG) for kw in result["missing"][:20]),
                        unsafe_allow_html=True,
                    )
            else:
                for label, passed, note in result["details"]:
                    icon = ":material/check_circle:" if passed else ":material/cancel:"
                    color_icon = theme.SUCCESS if passed else theme.DANGER
                    text = f":{'green' if passed else 'red'}[{label}]"
                    if note:
                        text += f"  \n:gray[{note}]"
                    st.markdown(text)


def _render_history():
    with st.container(border=True):
        st.subheader("Session History", anchor=False)
        st.caption("Resumes you've analyzed in this session")

        if not st.session_state.user_history:
            st.write(":gray[No resumes analyzed yet this session.]")
            return

        history_height = 280 if len(st.session_state.user_history) > 4 else "content"
        with st.container(height=history_height, border=False):
            for entry in st.session_state.user_history[:12]:
                color, bg = theme.score_color(entry["score"])
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{entry['name']}**  \n:gray[{entry['mode']} · {entry['time']}]")
                with c2:
                    st.markdown(badge_html(f"{entry['score']}%", color, bg), unsafe_allow_html=True)
                st.divider()
