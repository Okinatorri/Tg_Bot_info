import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------------- Логи ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- Переменные ----------------
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ---------------- Инициализация бота ----------------
# Создаем Application асинхронно
application = None

# ---------------- Команда /start ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = (
        "Привет! 👋\n\n"
        "Я простой Telegram бот, созданный для демонстрации работы с FastAPI.\n"
        "На данный момент у меня есть только одна команда - /start\n\n"
        "Приятного общения! 😊"
    )
    await update.message.reply_text(welcome_text)

# ---------------- FastAPI ----------------
app = FastAPI()

@app.on_event("startup")
async def startup():
    """Запуск приложения"""
    global application
    
    # Инициализируем бота
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем хендлеры
    application.add_handler(CommandHandler("start", start))
    
    # Инициализируем приложение
    await application.initialize()
    
    # Настраиваем вебхук
    webhook_url = "https://angel-camp.onrender.com/webhook"  # Замените на ваш URL
    await application.bot.set_webhook(webhook_url)
    logger.info(f"Webhook установлен: {webhook_url}")
    logger.info("Бот запущен!")

@app.post("/webhook")
async def webhook(request: Request):
    """Обработчик вебхуков от Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    """Корневой маршрут для проверки работы сервера"""
    return {"message": "Telegram Bot is running!"}

@app.get("/health")
async def health_check():
    """Маршрут для проверки здоровья приложения"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
