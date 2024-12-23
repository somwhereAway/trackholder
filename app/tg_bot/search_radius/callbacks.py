
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes
from geopy.distance import geodesic
import re

import constants


async def start_search_radius(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Введите координаты и радиус в формате:\n"
             "`XX.XXXXXN YY.YYYYYE ZZkm`",
        parse_mode="Markdown"
    )
    return constants.WAITING_INPUT


async def process_radius_input(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text

    match = re.match(
        r"^(\d+\.\d+)[Nn]\s+(\d+\.\d+)[Ee]\s+(\d+)[kK][mM]$",
        user_input
    )
    if not match:
        await update.message.reply_text(
            "Неверный формат данных. Попробуйте снова.")
        return constants.WAITING_INPUT

    lat, lon, radius_km = float(match.group(1)), float(
        match.group(2)), int(match.group(3))

    search_results = await search_objects_in_radius(lat, lon, radius_km)

    if not search_results:
        await update.message.reply_text(
            "Объекты в заданном радиусе не найдены.")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton(obj['name'], callback_data=f"obj_{obj['id']}")]
        for obj in search_results
    ]
    keyboard.append([InlineKeyboardButton("Скачать все объекты",
                    callback_data=f"download_all_{lat}_{lon}_{radius_km}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Найденные объекты:", reply_markup=reply_markup)
    return ConversationHandler.END


async def search_objects_in_radius(
        lat: float, lon: float, radius_km: int) -> list:
    objects = [
        {"id": 1, "name": "Объект 1", "coords": (55.751244, 37.618423)},
        {"id": 2, "name": "Объект 2", "coords": (56.751244, 38.618423)}
    ]

    results = []
    for obj in objects:
        distance = geodesic((lat, lon), obj["coords"]).km
        if distance <= radius_km:
            results.append(obj)

    return results

# Хэндлер отмены


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Команда отменена.")
    return ConversationHandler.END
