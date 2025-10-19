from flask import Flask, request
import asyncio
from aiogram import Bot, Dispatcher, types


bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

# Команда /start
@dp.message()
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Бот запущен на Render через Webhook.")

# Webhook для Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем JSON из запроса (не await!)
    update = types.Update.model_validate(request.get_json())
    
    # feed_update асинхронный, но Flask sync -> используем asyncio.run
    asyncio.run(dp.feed_update(bot, update))
    
    return "ok"  # Telegram ждёт любой 200-ответ

# Проверка доступности сервера
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

