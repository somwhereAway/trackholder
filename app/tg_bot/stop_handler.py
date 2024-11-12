from telegram import Update
from telegram.ext import ContextTypes

from core.crud import delete_user


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_id = update.message.from_user.id

    deleted = await delete_user(tg_id)
    text = ""
    if deleted:
        text = "Вы удалены из бд.\n" \
            "Все ваши файлы остались, но они больше"\
            "не связанны с вашей учетной записью."
    else:
        text = "Вы не зарегестрированны\n"
    await update.message.reply_html(text=text)
