# 🤖 ZenithMeet : AI-Powered Smart Meeting Scheduler

A smart group meeting scheduler that analyze natural language chats and automatically schedules meetings based on **time**, **venue**, and **participants**. It also sends **email confirmations** to all attendees using.

## 🚀 Features

- ✅ Chat-based group interaction
- 🧠 Gemini AI to detect date, time & venue from chat
- 📅 One-click meeting scheduling
- 📧 Email confirmation to all participants
- 🗂️ SQLite database for users, messages & meetings
- 🎯 Built with Python + Streamlit

---

## 📂 Project Structure

```
├── backend/
│   ├── chat_handler.py       # Handles DB operations (users, messages, meetings)
│   ├── gemini_agent.py       # Uses Gemini to extract meeting info from chat
│   ├── meeting_logic.py      # Central logic to parse, validate, and schedule meeting
│   ├── emailer.py            # Sends email to participants
│   └── db.py                 # Initializes the database (SQLite)
│
├── data/
│   └── chat.db               # SQLite DB file
│
├── main.py                   # Streamlit frontend UI
├── .env                      # Environment variables (Gmail credentials, Gemini API key)
└── README.md                 # You’re here!
```

---

## 🧠 Gemini Prompt Format

Gemini AI receives the chat history and responds in this structured format:
```json
{
  "availability": {
    "Abhinav": "2025-08-04T19:00:00",
    "Nimul": "2025-08-04T19:00:00"
  },
  "place": "Coke Cafe"
}
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/imabhnv/ZenithMeet.git
cd ai-meeting-scheduler
```

### 2. Create and Fill `.env`

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_password_or_app_pass
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run main.py
```

---

## 🧪 Example Workflow

1. Register yourself with name and email
2. Chat with other users like:  
   `"Let's meet tomorrow at 6 PM at @ Coke Cafe"`  
3. Click 📅 "Schedule Meeting"
4. Gemini analyzes the conversation, schedules the meeting, and sends emails 🎉

---

## 💌 Email Format

```
Namaste Abhinav,

Your group meeting has been successfully scheduled.

📅 Date & Time: 2025-08-04 07:00 PM IST
📍 Venue: Coke Cafe
👥 Participants: Abhinav, Nimul

Please be on time.

- AI Meeting Scheduler 🤖
```

---

## 🙌 Credits

Built with ❤️ by Abhinav Varshney using:
- Google Gemini Pro (via `google.generativeai`)
- Streamlit
- SMTP (Gmail)
- SQLite3

---

## 📃 License

This project is open-source and free to use for educational purposes.
