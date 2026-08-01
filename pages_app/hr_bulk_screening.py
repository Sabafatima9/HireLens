"""
pages_app/hr_bulk_screening.py
HR Portal - Bulk Screening: upload a ZIP of CVs, score them all against
a threshold (with or without a JD), and review/edit results in a table.
Uses st.status() for a live, expandable processing log.
"""

import io
import os
import tempfile
import zipfile

import streamlit as st
import pandas as pd

import cv_parser
import ats_scorer


def render():
    st.subheader("Bulk Resume Screening", anchor=False)
    st.caption("Upload a ZIP of CVs to score them all at once")

    with st.container(border=True):
        uploaded_zip = st.file_uploader("Upload a ZIP of CVs", type=["zip"], label_visibility="collapsed")

        col1, col2 = st.columns([2, 1])
        with col1:
            use_jd = st.toggle("Score against a Job Description", key="hr_jd_toggle", value=st.session_state.use_jd_hr)
        with col2:
            threshold = st.number_input("Reject if score below (%)", min_value=0, max_value=100,
                                         value=st.session_state.threshold, step=5)

        jd_text = ""
        if use_jd:
            jd_text = st.text_area("Paste the Job Description", height=140, key="hr_jd_text",
                                    value=st.session_state.jd_text_hr)

        process = st.button("Process All CVs", type="primary", icon=":material/bolt:")

    if process:
        _process_zip(uploaded_zip, use_jd, jd_text, threshold)

    if st.session_state.candidates:
        _render_table()
    else:
        st.write(":gray[No results yet. Upload a ZIP and click **Process All CVs**.]")


def _process_zip(uploaded_zip, use_jd, jd_text, threshold):
    if not uploaded_zip:
        st.warning("Please upload a zip file of CVs first.")
        return

    if use_jd and not jd_text.strip():
        st.warning("Please paste a job description, or turn the toggle off.")
        return

    st.session_state.use_jd_hr = use_jd
    st.session_state.jd_text_hr = jd_text
    st.session_state.threshold = threshold

    extract_dir = tempfile.mkdtemp(prefix="ats_cvs_")
    try:
        with zipfile.ZipFile(io.BytesIO(uploaded_zip.getvalue())) as zf:
            zf.extractall(extract_dir)
    except zipfile.BadZipFile:
        st.error("This doesn't look like a valid zip file.")
        return

    cv_files = []
    for root_dir, _, files in os.walk(extract_dir):
        for fname in files:
            if fname.lower().endswith((".pdf", ".docx")):
                cv_files.append(os.path.join(root_dir, fname))

    if not cv_files:
        st.warning("No .pdf or .docx files were found in that zip.")
        return

    candidates = []
    with st.status(f"Scoring {len(cv_files)} CV(s)...", expanded=True) as status:
        for path in cv_files:
            fname = os.path.basename(path)
            try:
                text = cv_parser.extract_text(path)
            except Exception:
                st.write(f":gray[Skipped {fname} — couldn't read file]")
                continue
            if not text.strip():
                st.write(f":gray[Skipped {fname} — no extractable text]")
                continue

            email = cv_parser.extract_email(text)
            name = cv_parser.extract_name(text, fallback_filename=path)

            result = ats_scorer.score_against_jd(text, jd_text) if use_jd else ats_scorer.score_general(text)
            score = result["score"]
            status_label = "Reject" if score < threshold else "Pass"

            icon = ":green[✓]" if status_label == "Pass" else ":red[✗]"
            st.write(f"{icon} **{name}** — {score}%")

            candidates.append({"name": name, "email": email or "", "score": score, "status": status_label})

        status.update(label=f"Done — {len(candidates)} CV(s) scored", state="complete", expanded=False)

    st.session_state.candidates = candidates
    rejected_count = sum(1 for c in candidates if c["status"] == "Reject")
    st.toast(f"Processed {len(candidates)} CV(s) · {rejected_count} flagged for rejection", icon=":material/task_alt:")


def _render_table():
    st.markdown("#### Results")
    st.caption("Double-click the Email column to fix any email that wasn't extracted correctly.")

    df = pd.DataFrame(st.session_state.candidates)[["name", "email", "score", "status"]]
    df.columns = ["Candidate Name", "Email", "ATS Score", "Status"]

    edited = st.data_editor(
        df,
        column_config={
            "Candidate Name": st.column_config.TextColumn(disabled=True),
            "Email": st.column_config.TextColumn(),
            "ATS Score": st.column_config.ProgressColumn(
                format="%d%%", min_value=0, max_value=100
            ),
            "Status": st.column_config.SelectboxColumn(options=["Pass", "Reject"]),
        },
        hide_index=True,
        width='stretch',
        key="candidates_editor",
    )

    # sync any manual edits (email fixes, manual status overrides) back into session state
    for i, row in edited.iterrows():
        st.session_state.candidates[i]["email"] = row["Email"]
        st.session_state.candidates[i]["status"] = row["Status"]
