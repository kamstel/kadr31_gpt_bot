import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

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
    await update.message.reply_text(
        "🎬 Привет! Я бот-видеомейкер. Хочешь идею для Reels, сценарий или помощь с монтажом? Пиши!"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен 🚀")
    app.run_polling()