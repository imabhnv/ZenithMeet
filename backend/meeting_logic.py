from datetime import datetime
from backend.chat_handler import get_chat_history, get_email_by_name
from backend.gemini_agent import extract_meeting_details

def try_schedule_meeting():
    history = get_chat_history()
    chat_text = "\n".join([f"{row['name']}: {row['message']}" for row in history])

    parsed_data = extract_meeting_details(chat_text)

    if not parsed_data or "availability" not in parsed_data:
        return False, "❌ Gemini failed to extract meeting details.", None

    names = list(parsed_data["availability"].keys())
    time_str = list(parsed_data["availability"].values())[0]
    dt = datetime.fromisoformat(time_str)
    venue = parsed_data.get("place", "")

    participants = []
    missing = []

    for name in names:
        email = get_email_by_name(name)
        if email:
            participants.append(email)
        else:
            missing.append(name)

    if missing:
        return False, f"❌ Could not find emails for: {', '.join(missing)}", None

    return True, "✅ Gemini parsed meeting data.", {
        "time": dt,
        "place": venue,
        "participants": participants
    }