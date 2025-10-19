import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
import os

# 🔹 токен
API_TOKEN = os.getenv("BOT_TOKEN")

# 🔹 webhook URL — сюда Telegram будет слать обновления
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask(__name__)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Бот запущен на Render через Webhook.")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = types.Update.model_validate(request.get_json())
    asyncio.run(dp.feed_update(bot, update))
    return "ok", 200


@app.route("/")
def home():
    return "Бот работает ✅"

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.run(on_startup())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

