from flask import Flask, request
import requests
from bot.config import BASE_URL, PORT
from bot.db import init_db
from bot.handlers import handle_start, handle_text

def get_updates(data):
    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    user_id = msg.get("from", {}).get("id")
    text = msg.get("text", "")
    return chat_id, user_id, text

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Bot is running ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id, user_id, text = get_updates(data)
    if text == "/start":
        reply = handle_start()
    else:
        reply = handle_text(user_id, text)
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)