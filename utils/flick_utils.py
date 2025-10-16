# ----------------------------------------
# Functions that are used in all projects
# ----------------------------------------

#importing modules
import re
import html
import os
import time
import random
import smtplib
import datetime
from datetime import timezone
from dotenv import load_dotenv
from flask import request,session

#logging errors and users
#to store errors for debugging
def log_error(message):
    with open("DB/error.log", "a",encoding='utf-8') as log_file:
        log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

#logging activity
def log_activity(action):
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_id = session.get('user_id', 'Unknown')
        username = session.get('username', 'Guest')
    except RuntimeError:
        ip = "NoRequest"
        user_id = "NoSession"
        username = "Unknown"

    timestamp = datetime.now(timezone.utc).strftime("[%Y-%m-%d %H:%M:%S UTC]")

    entry = f"{timestamp} [ACTIVITY] [IP: {ip}] [UserID: {user_id}] [Username: {username}] {action}"


#working with files
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a',"jpeg","png","jpg","heic","webm"}
#to check if file is correct
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#mailer functuanlity

#State making
load_dotenv()
APP_PASSWORD = os.getenv("APP_PASSWORD")
APP_EMAIL = os.getenv("APP_EMAIL")


def check_required_env_keys(*keys):
    for key in keys:
        if not os.getenv(key):
            raise EnvironmentError(f"Missing required environment variable: {key}")


#to sanitaze the data
def sanitize_message_for_ai(message: str) -> str:
    """
    Cleans the message before sending to AI. 
    Removes harmful characters, scripts, and limits length.
    """
    message = message.strip()
    message = html.unescape(message)                    # Unescape any HTML entities
    message = re.sub(r"<.*?>", "", message)             # Remove any HTML tags
    message = re.sub(r"[^\w\s.,!?@'\"-]", "", message)  # Allow some punctuation
    message = re.sub(r"\s+", " ", message)              # Collapse excessive whitespace
    return message[:500]                                # Cap to 500 chars


#to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

#sending mails
def send_email(rece_mail, content,subject=""):
    check_required_env_keys(APP_EMAIL,APP_PASSWORD)
    try:
         to_email=rece_mail
         msg = content
         msg['Subject'] = subject
         msg['From'] = APP_EMAIL
         msg['To'] = to_email
         msg.set_content(content)

         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
             smtp.login(APP_EMAIL, APP_PASSWORD)
             smtp.send_message(msg)
    except Exception as e:
        log_error(f"{e} in send_email in male")
        return ""
