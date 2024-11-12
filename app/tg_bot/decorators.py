from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext

from core.crud import is_user_registered


def require_registration(func):
    @wraps(func)
    async def wrapper(
        update: Update, context: CallbackContext, *args, **kwargs
    ):
        user_id = update.message.from_user.id
        if not await is_user_registered(user_id):
            await update.message.reply_text(
                "Пожалуйста, зарегистрируйтесь. Для этого скомандуйте /start.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
