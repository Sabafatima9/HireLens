"""
email_sender.py
Sends rejection emails via SMTP (Gmail App Password by default).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, sender_email, app_password, smtp_host="smtp.gmail.com", smtp_port=587):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def test_connection(self):
        """Tries to log in without sending anything. Raises on failure."""
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)
        return True

    def send_email(self, to_email, subject, body):
        """Sends a single email. Returns (success: bool, error_message: str|None)."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())

            return True, None
        except Exception as e:
            return False, str(e)

    def send_bulk(self, recipients, subject_template, body_template, progress_callback=None):
        """
        recipients: list of dicts, each with at least "name" and "email"
        subject_template / body_template: strings that may contain {name}
        progress_callback: optional function(index, total, name, success, error)
        Returns list of results: [{name, email, success, error}]
        """
        results = []
        total = len(recipients)

        for i, candidate in enumerate(recipients, start=1):
            name = candidate.get("name", "Candidate")
            email = candidate.get("email")

            if not email:
                results.append({"name": name, "email": None, "success": False, "error": "No email found"})
                if progress_callback:
                    progress_callback(i, total, name, False, "No email found")
                continue

            subject = subject_template.replace("{name}", name)
            body = body_template.replace("{name}", name)

            success, error = self.send_email(email, subject, body)
            results.append({"name": name, "email": email, "success": success, "error": error})

            if progress_callback:
                progress_callback(i, total, name, success, error)

        return results
