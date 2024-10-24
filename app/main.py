fast_api
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Update

import tg_bot.tgbot_core as tgbot_core
app = FastAPI()

templates = Jinja2Templates(directory="templates")

requests_list = []


@app.post("/webhook/")
async def handle_webhook(request: Request):
    data = await request.json()  # Получаем данные в формате JSON
    requests_list.append(data)  # Сохраняем запрос в список
    await tgbot_core.tgbot.ptb_app.update_queue.put(
        Update.de_json(
            data=data, bot=tgbot_core.tgbot.ptb_app.bot
        )
    )
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def get_requests(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "requests": requests_list})


async def main():
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8000,
            use_colors=True,
            host='localhost',
        )
    )
    async with tgbot_core.tgbot.ptb_app:
        await tgbot_core.tgbot.ptb_app.start()
        await webserver.serve()
        await tgbot_core.tgbot.ptb_app.stop()


if __name__ == '__main__':
    asyncio.run(main())
=======
import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters)

from app.file_handle import handle_document, get_my_merged_kml
from app.start_handler import start


load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(
        TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("my_merged", get_my_merged_kml))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(
        filters.Document.ALL, handle_document))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
dev
