import sqlite3
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "chat.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scheduled_time TEXT,
            location TEXT,
            participants TEXT,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()

def add_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        return row["id"]

    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    return cursor.lastrowid

def get_user_name_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result["name"] if result else None

def get_email_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result["email"] if result else None

def save_message(user_id, message):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages (user_id, message, timestamp) VALUES (?, ?, ?)",
                   (user_id, message, timestamp))
    conn.commit()

def get_chat_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT messages.message, messages.timestamp, users.name, users.email
        FROM messages
        JOIN users ON messages.user_id = users.id
        ORDER BY messages.timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_chat_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()

def save_meeting_to_db(participants, scheduled_time, location, created_by=None):
    conn = get_connection()
    cursor = conn.cursor()

    creator_id = None
    if created_by:
        cursor.execute("SELECT id FROM users WHERE email = ?", (created_by,))
        row = cursor.fetchone()
        if row:
            creator_id = row["id"]

    participants_str = ",".join(participants)
    cursor.execute("""
        INSERT INTO meetings (scheduled_time, location, participants, created_by)
        VALUES (?, ?, ?, ?)
    """, (scheduled_time.isoformat(), location, participants_str, creator_id))
    conn.commit()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    return cursor.fetchall()

def delete_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    return changes > 0  