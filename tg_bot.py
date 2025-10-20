import os
import logging
from contextlib import asynccontextmanager
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

# ---------------- Инициализация приложения ----------------
telegram_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global telegram_app
    
    try:
        # Инициализируем Telegram приложение
        telegram_app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        telegram_app.add_handler(CommandHandler("start", start))
        
        # Инициализируем
        await telegram_app.initialize()
        
        # Настраиваем вебхук
        webhook_url = "https://angel-camp.onrender.com/webhook"  # ЗАМЕНИТЕ на ваш реальный URL
        await telegram_app.bot.set_webhook(webhook_url)
        
        logger.info("Бот успешно запущен!")
        logger.info(f"Webhook установлен: {webhook_url}")
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise
    
    yield
    
    # Shutdown
    if telegram_app:
        await telegram_app.shutdown()

# ---------------- FastAPI ----------------
app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: Request):
    """Обработчик вебхуков от Telegram"""
    if telegram_app is None:
        return {"status": "error", "message": "Application not initialized"}
    
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
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

