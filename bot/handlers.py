# bot/handlers.py
def handle_start():
    return "Привет! Я бот для отслеживания задач."

def handle_text(user_id, text):
    return f"Вы написали: {text}" 