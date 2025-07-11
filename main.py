import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Создаем диспетчер и регистрируем команды
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

def start(update: Update, context):
    update.message.reply_text("Привет! Я жив и работаю через webhook 🚀")

dispatcher.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Бот работает. Всё огонь 🔥"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

# Запуск двух потоков: Flask и Telegram
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram_bot()
