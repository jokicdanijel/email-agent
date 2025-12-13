import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")

try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
except ValueError as e:
    raise ValueError(f"Invalid port configuration: {e}")