"""
settings_manager.py
Stores HR's sender email + app password locally in settings.json
so they don't have to retype it every time.

NOTE: this is plaintext local storage, meant for a single HR user's own
machine. If this project is pushed to GitHub, settings.json MUST be
added to .gitignore so the password is never uploaded.
"""

import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

DEFAULTS = {
    "sender_email": "",
    "app_password": "",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULTS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = DEFAULTS.copy()
        merged.update(data)
        return merged
    except (json.JSONDecodeError, OSError):
        return DEFAULTS.copy()


def save_settings(sender_email, app_password, smtp_host="smtp.gmail.com", smtp_port=587):
    data = {
        "sender_email": sender_email,
        "app_password": app_password,
        "smtp_host": smtp_host,
        "smtp_port": smtp_port,
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data
