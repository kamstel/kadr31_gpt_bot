from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET_PATH", "webhook")

app = Flask(__name__)

bot_app = ApplicationBuilder().token(TOKEN).build()

# Пример команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я живой 🤖")

# Регистрируем хендлер
bot_app.add_handler(CommandHandler("start", start))


@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "ok"


# Flask "ping" маршрут для проверки доступности
@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"


if __name__ == "__main__":
    import asyncio

    # Запускаем Flask
    port = int(os.environ.get("PORT", 5000))
    asyncio.run(bot_app.initialize())  # Инициализация
    app.run(host="0.0.0.0", port=port)
