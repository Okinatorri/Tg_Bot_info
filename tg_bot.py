from flask import Flask, request, jsonify
import asyncio
import os
from aiogram import Bot, Dispatcher, types

# Получаем токен из переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

app = Flask(__name__)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Берем глобальный event loop
loop = asyncio.get_event_loop()


# Пример команды /start
@dp.message()
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Бот запущен на Render через Webhook.")


# Webhook обработчик
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    update = types.Update.model_validate(data)

    # feed_update запускаем через create_task, loop живой, не закрываем его
    asyncio.create_task(dp.feed_update(bot, update))

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
