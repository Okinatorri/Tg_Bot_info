import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import logging

# ---------------- Логи ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- Переменные ----------------
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-app.onrender.com/webhook

# ---------------- Инициализация ----------------
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

# ---------------- Хендлеры ----------------
@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Привет! Я минимальный бот на FastAPI и Aiogram 3 🎉")

@dp.message()
async def echo_handler(message: types.Message):
    # Просто повторяем текст
    await message.answer(f"Ты написал: {message.text}")


# ---------------- FastAPI ----------------
@app.on_event("startup")
async def startup():
    # Инициализация диспетчера
    await dp.startup()
    # Устанавливаем webhook
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook установлен: {WEBHOOK_URL}")

@app.on_event("shutdown")
async def shutdown():
    await dp.shutdown()
    await bot.session.close()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    # Обработка update через диспетчер
    await dp.feed_update(bot, update)
    return {"status": "ok"}


# ---------------- Запуск локально ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
