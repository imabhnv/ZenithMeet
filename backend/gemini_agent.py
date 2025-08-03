from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import json
import streamlit as st

load_dotenv()
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def extract_meeting_details(chat_text):
    today = datetime.now().strftime("%Y-%m-%d") 

    prompt = f"""
You're an AI meeting assistant. Today is {today}. Based on the conversation below, extract:
- Participants' names and their preferred meeting time (in ISO format).
- The proposed venue.

Return your output **strictly in valid JSON** format as:
{{
  "availability": {{
    "Name1": "YYYY-MM-DDTHH:MM:SS",
    "Name2": "YYYY-MM-DDTHH:MM:SS"
  }},
  "place": "Venue name or null"
}}

Chat History:
\"\"\"
{chat_text}
\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().strip("```json").strip("```")
        return json.loads(json_text)
    except Exception as e:
        print("❌ Gemini parsing failed:", e)
        return {}
