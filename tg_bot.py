import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from flask import Flask, request
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен из переменных окружения Render
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)

# === Команда /start ===
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("✅ Бот успешно запущен на Render!")

# === Flask endpoint ===
@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = types.Update.model_validate(await request.get_json())
    await dp.feed_update(bot, update)
    return {"ok": True}

# === Установка вебхука ===
async def on_startup():
    webhook_url = "https://angel-camp.onrender.com/webhook"
    await bot.set_webhook(webhook_url)

if __name__ == '__main__':
    asyncio.run(on_startup())  # ставим вебхук
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
