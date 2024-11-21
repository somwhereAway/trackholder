from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from tg_bot.admin_menu import constants as cs


async def main_keyboard() -> list[list[InlineKeyboardButton]]:
    keyboard = [
        [
            InlineKeyboardButton(
                "Показать пользователей",
                callback_data=cs.SHOW_USER
            ),
        ]
    ]
    keyboard.append(
        [InlineKeyboardButton('выйти', callback_data=cs.EXIT)]
    )
    return keyboard


async def paginated_users_keyboard(
    all_items: list[dict],
    page: int
) -> list[list[InlineKeyboardButton]]:
    start_index = page * cs.ITEMS_PER_PAGE
    end_index = start_index + cs.ITEMS_PER_PAGE
    items = all_items[start_index:end_index]
    if not all_items:
        keyboard = [
            [InlineKeyboardButton('выйти', callback_data=cs.EXIT)]
        ]
        return keyboard
    keyboard = []
    for item in items:
        item_text = '||'.join(
            [f'{key}: {value}' for key, value in item.items()])

        keyboard.append(
            [InlineKeyboardButton(
                item_text, callback_data=cs.CURR_USER + f'{item["id"]}')
             ]
        )
        keyboard.append([])
        if page > 0:
            keyboard[-1].append(InlineKeyboardButton(
                'Предыдущая', callback_data=f'page_{page-1}'))
        if end_index < len(all_items):
            keyboard[-1].append(InlineKeyboardButton(
                'Следующая', callback_data=f'page_{page+1}'))
        keyboard.append(
            [InlineKeyboardButton('выйти', callback_data=cs.EXIT)]
        )
        return keyboard


async def represent_user_keyboard(
        tg_id: int
) -> list[list[InlineKeyboardButton]]:
    keyboard = [
        [InlineKeyboardButton(
            'сделать супером', callback_data=cs.MAKE_SUPER + str(tg_id))],
        [InlineKeyboardButton(
            'понизить до обычного', callback_data=cs.MAKE_COMMON + str(tg_id))],
        [InlineKeyboardButton('выйти', callback_data=cs.EXIT)]
    ]
    return keyboard
