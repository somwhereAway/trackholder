import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes

)
from dotenv import load_dotenv

from tg_bot.start_handler import start
from tg_bot.stop_handler import stop
from tg_bot.file_handle import handle_document, get_my_merged_kml

load_dotenv()

TOKEN = os.environ['TOKEN']


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f'Вы написали: {text}')


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application.builder()
            .token(TOKEN)
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(CommandHandler("start", start))
        self.ptb_app.add_handler(CommandHandler("stop", stop))
        self.ptb_app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, handle_message))
        self.ptb_app.add_handler(MessageHandler(
            filters.Document.ALL, handle_document))
        self.ptb_app.add_handler(CommandHandler(
            "my_merged", get_my_merged_kml))


tgbot = TGBot()
