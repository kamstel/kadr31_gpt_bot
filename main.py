import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
import threading

# Настройка Telegram и OpenAI
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Flask сервер для Render
app = Flask(__name__)

@app.route("/")
def home():
    return "I'm alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Логика Telegram-бота
async def chat_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": "Ты креативный видеомейкер. Помогаешь с Reels, монтажом, сценарием, заголовками и продвижением. Отвечай как живой человек — с юмором, коротко, по делу и без воды."},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = await chat_with_gpt(text)
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Привет! Я бот-видеомейкер. Хочешь идею для Reels, сценарий или помощь с монтажом? Пиши!")

def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен 🚀")
    application.run_polling()

# Запуск двух потоков: Flask и Telegram
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram_bot()