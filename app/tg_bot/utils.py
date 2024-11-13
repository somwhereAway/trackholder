from telegram import Update


async def delete_file_reply_text(update: Update, text: str):
    await update.message.delete()
    await update.message.reply_text(text)
