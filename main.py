import os
import sqlite3
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# === Database ===
DB_NAME = "tasks.db"
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        text TEXT,
                        done BOOLEAN DEFAULT 0
                    )""")
        conn.commit()

# === Handlers ===
def handle_start(chat_id):
    return "Привет! Отправь мне задачу, и я её запомню."

def handle_text(chat_id, user_id, text):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
        conn.commit()
    return f"Задача добавлена: {text}"

def get_updates(data):
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_id = msg.get("from", {}).get("id")
    text = msg.get("text", "")
    return chat_id, user_id, text

# === Routes ===
@app.route("/", methods=["GET"])
def root():
    return "Bot is running ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id, user_id, text = get_updates(data)
    if text == "/start":
        reply = handle_start(chat_id)
    else:
        reply = handle_text(chat_id, user_id, text)
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))