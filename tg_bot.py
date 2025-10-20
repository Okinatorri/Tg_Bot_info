import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = (
        "Привет! Все работает нормально."
    )
    await update.message.reply_text(welcome_text)


telegram_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global telegram_app
    
    try:
        
        telegram_app = Application.builder().token(TOKEN).build()
        
        
        telegram_app.add_handler(CommandHandler("start", start))
        
        
        await telegram_app.initialize()
        
        # Настр
        webhook_url = "https://angel-camp.onrender.com/webhook" 
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

