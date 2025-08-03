import smtplib
from email.message import EmailMessage
from datetime import datetime
from pytz import timezone
from backend.chat_handler import get_user_name_by_email
import streamlit as st

EMAIL_ADDRESS = st.secrets["EMAIL_USER"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASS"]
IST = timezone("Asia/Kolkata")

def send_confirmation_email(participants, scheduled_time, meeting_place=None):
    success = True

    if isinstance(scheduled_time, str):
        scheduled_time = datetime.fromisoformat(scheduled_time)
    if scheduled_time.tzinfo is None:
        scheduled_time = IST.localize(scheduled_time)
    else:
        scheduled_time = scheduled_time.astimezone(IST)

    date_str = scheduled_time.strftime("%Y-%m-%d %I:%M %p") + " IST"
    venue_str = meeting_place or "To be decided"

    email_to_name = {e: get_user_name_by_email(e) or e.split("@")[0] for e in participants}
    name_list = ", ".join(email_to_name.values())

    for email in participants:
        try:
            msg = EmailMessage()
            msg["Subject"] = "📅 Meeting Confirmation - AI Scheduler"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            user_name = email_to_name.get(email)

            msg.set_content(f"""
Namaste {user_name},

Your group meeting has been successfully scheduled.

📅 Date & Time: {date_str}
📍 Venue: {venue_str}
👥 Participants: {name_list}

Please be on time.

- AI Meeting Scheduler 🤖
            """.strip())

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            print(f"✅ Email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send email to {email}: {e}")
            success = False

    return success
