import os
from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext
from dotenv import load_dotenv

from core.crud import is_user_registered, is_superuser

load_dotenv()

ADMIN_ID = os.environ['ADMIN_ID']


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


def require_superuser(func):
    @wraps(func)
    async def wrapper(
        update: Update, context: CallbackContext, *args, **kwargs
    ):
        user_id = update.message.from_user.id
        if not await is_superuser(user_id):
            await update.message.reply_text(
                "Команда недоступна. Обратитесь к администратору.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def require_administrator(func):
    @wraps(func)
    async def wrapper(
        update: Update, context: CallbackContext, *args, **kwargs
    ):
        user_id = update.message.from_user.id
        if user_id != int(ADMIN_ID):
            await update.message.reply_text(
                "Команда недоступна.Вы не админ!")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
