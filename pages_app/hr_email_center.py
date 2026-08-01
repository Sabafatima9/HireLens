"""
pages_app/hr_email_center.py
HR Portal - Email Automation Center: configure sender email, edit the
rejection template, review the reject list in a modal, and send only
after HR explicitly confirms.
"""

import streamlit as st
import pandas as pd

import settings_manager
from email_sender import EmailSender

DEFAULT_SUBJECT = "Application Update - {name}"
DEFAULT_BODY = (
    "Dear {name},\n\n"
    "Thank you for applying and for the time you invested in your application. "
    "After careful review, we have decided to move forward with other candidates "
    "whose profiles more closely match this role's requirements at this time.\n\n"
    "We appreciate your interest and encourage you to apply for future openings "
    "that match your background.\n\n"
    "Best regards,\nHR Team"
)


def render():
    st.subheader("Email Automation Center", anchor=False)
    st.caption("Configure and send rejection emails")

    settings = settings_manager.load_settings()

    with st.container(border=True):
        st.markdown("#### Sender Account")
        col1, col2 = st.columns(2)
        with col1:
            sender_email = st.text_input("Sender email", value=settings["sender_email"])
        with col2:
            app_password = st.text_input("App password", value=settings["app_password"], type="password")

        st.caption(
            "For Gmail: enable 2-Step Verification, then generate an App Password at "
            "myaccount.google.com/apppasswords"
        )

        if st.button("Save Settings", icon=":material/save:"):
            settings_manager.save_settings(sender_email.strip(), app_password.strip())
            st.toast("Email settings saved", icon=":material/check_circle:")

    with st.container(border=True):
        st.markdown("#### Rejection Email Template")
        st.caption("Use {name} as a placeholder")
        subject = st.text_input("Subject", value=DEFAULT_SUBJECT, key="email_subject")
        body = st.text_area("Body", value=DEFAULT_BODY, height=200, key="email_body")

    with st.container(border=True):
        rejected = [c for c in st.session_state.candidates if c["status"] == "Reject"]
        st.write(f"**{len(rejected)}** candidate(s) currently marked for rejection.")

        if st.button("Review & Send Rejection Emails", type="primary", icon=":material/send:"):
            if not rejected:
                st.warning("No candidates are currently marked as Reject. Run Bulk Screening first.")
            else:
                settings_now = settings_manager.load_settings()
                if not settings_now["sender_email"] or not settings_now["app_password"]:
                    st.warning("Please save your sender email and app password above first.")
                else:
                    _confirm_send_dialog(rejected, settings_now, subject, body)


@st.dialog("Confirm Rejection Emails", width="large")
def _confirm_send_dialog(rejected, settings, subject_template, body_template):
    st.markdown(f"**About to email {len(rejected)} candidate(s):**")

    df = pd.DataFrame(rejected)[["name", "email", "score"]]
    df.columns = ["Name", "Email", "Score"]
    df["Email"] = df["Email"].replace("", "No email — will be skipped")
    st.dataframe(df, hide_index=True, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm & Send", type="primary", width='stretch', icon=":material/send:"):
            _send_emails(rejected, settings, subject_template, body_template)
            st.rerun()
    with col2:
        if st.button("Cancel", width='stretch', icon=":material/close:"):
            st.rerun()


def _send_emails(rejected, settings, subject_template, body_template):
    sender = EmailSender(settings["sender_email"], settings["app_password"],
                          settings["smtp_host"], settings["smtp_port"])

    results = []
    with st.status("Sending rejection emails...", expanded=True) as status:
        def on_progress(i, total, name, success, error):
            icon = ":green[✓]" if success else ":red[✗]"
            st.write(f"{icon} ({i}/{total}) {name}" + (f" — {error}" if error else ""))

        results = sender.send_bulk(rejected, subject_template, body_template, progress_callback=on_progress)

        failed = [r for r in results if not r["success"]]
        if failed:
            status.update(label=f"Done with {len(failed)} failure(s)", state="error", expanded=True)
        else:
            status.update(label=f"Sent {len(results)} email(s) successfully", state="complete", expanded=False)

    st.session_state.last_send_results = results
    failed = [r for r in results if not r["success"]]

    if failed:
        st.warning(f"{len(failed)} email(s) failed. Check the sender account settings and try again.")
    else:
        st.toast(f"Sent {len(results)} rejection email(s)", icon=":material/mark_email_read:")
