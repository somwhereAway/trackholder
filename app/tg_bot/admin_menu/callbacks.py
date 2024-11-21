import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler


from tg_bot.admin_menu.keyboards import (
    paginated_users_keyboard,
    represent_user_keyboard,
    main_keyboard
)
from core.crud import get_all_users, get_user, update_user
from core.models import TelegramUser
from tg_bot.admin_menu import constants as cs
from tg_bot.decorators import require_administrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@require_administrator
async def admin_panel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started admin menu.", user.first_name)
    keyboard = await main_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет, Админ!", reply_markup=reply_markup)
    return cs.USER_MENU


@require_administrator
async def users_panel(update: Update, context: CallbackContext):
    users: list[TelegramUser] = await get_all_users()
    page = 0
    users_list = []
    for user in users:
        users_list.append(
            {
                'id': user.tg_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
            }
        )
    context.user_data['all_users'] = users_list
    return await show_users(update, context, page)


@require_administrator
async def show_users(update: Update, context: CallbackContext, page):
    query = update.callback_query
    await query.answer()
    users = context.user_data['all_users']
    if users:
        message_text = 'вот:'
    else:
        message_text = 'Никого нет, даже тебя!'
    reply_markup = InlineKeyboardMarkup(
        await paginated_users_keyboard(users, page)
    )
    await query.edit_message_text(
        text=message_text, reply_markup=reply_markup
    )
    return cs.USER_MENU


@require_administrator
async def rep_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data

    if query_data.startswith('page_'):
        page = int(query_data.split('_')[1])
        await show_users(update, context, page)
    if query_data.startswith(cs.EXIT):
        return ConversationHandler.END


@require_administrator
async def represent_user(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data
    tg_id = int(query_data.split('_')[1])
    user = await get_user(tg_id)

    if user:
        user_info = "\n".join(
            [
                f"{field}: {getattr(user, field)}" for field in user.__table__.columns.keys()]
        )
        text = f"Информация о пользователе:\n\n{user_info}"
        reply_markup = InlineKeyboardMarkup(
            await represent_user_keyboard(tg_id)
        )
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    else:
        # Если пользователь не найден
        await query.edit_message_text("Пользователь не найден.")


async def make_super(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data
    tg_id = int(query_data.split('_')[1])
    superuser_str = query_data.split('_')[0] + '_'
    if superuser_str == cs.MAKE_SUPER:
        updates = {
            "superuser": True
        }
    elif superuser_str == cs.MAKE_COMMON:
        updates = {
            "superuser": False
        }
    else:
        return await represent_user(update, context)
    await update_user(tg_id, updates)
    return await represent_user(update, context)


async def exit_conversation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    try:
        await query.delete_message()
    except Exception as e:
        print(f"Error deleting message: {e}")

    return ConversationHandler.END
