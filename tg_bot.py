import asyncio
import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + "/webhook"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask(__name__)

loop = asyncio.get_event_loop()  # создаём event loop один раз

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Бот запущен на Render через Webhook.")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = types.Update.model_validate(request.get_json())
    asyncio.ensure_future(dp.feed_update(bot, update), loop=loop)
    return "ok", 200

@app.route("/")
def home():
    return "Бот работает через Render ✅"

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

if __name__ == "__main__":
    loop.run_until_complete(on_startup())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
