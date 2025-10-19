import os
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher, types
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Telegram token is not set!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

# ==========================
# Команда /start
# ==========================
@dp.message()
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Бот запущен на Render через Webhook.")

# ==========================
# Webhook
# ==========================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "no data"}), 400

    update = types.Update.model_validate(data)
    
    # Здесь не asyncio.run, а безопасный способ через loop
    loop = asyncio.get_event_loop()
    loop.create_task(dp.feed_update(bot, update))

    return jsonify({"status": "ok"}), 200

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
