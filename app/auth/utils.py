from bcrypt import hashpw, gensalt
from sqlalchemy import Column
import smtplib
from email.mime.text import MIMEText
import os
from typing import Optional

subject = "Reset Password"
body = "Here is the token to reset your password.  Please use it within the next 15 minutes."
recipients = []
password = os.getenv("EMAIL_PASSWORD")
def send_reset_email(recipient_email: str, subject: str = subject, body: str = body, token: Optional[str] = None):
    body = f"""
Hi,

We received a request to reset your password.

Please use the following token to reset your password. This token is valid for 15 minutes:

Token: {token}

If you didn't request this, you can safely ignore this email.

Thanks,
Your Team
"""
    sender = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"Your App Team <{sender}>"
    msg["To"] = recipient_email

    if password is None:
        print("Error: EMAIL_PASSWORD environment variable is not set.")
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, [recipient_email], msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def password_validity(password: str) -> bool:
    """
    Validate the password based on specific criteria.
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    import re

    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def generate_password_hash(password: str) -> str:
    """
    Generate a hashed password using a secure hashing algorithm.
    """ 
    if not password_validity(password):
        raise ValueError("Password does not meet complexity requirements.")
    
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed.decode('utf-8')

def check_password(hashed_password: Column[str], password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    return hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')

