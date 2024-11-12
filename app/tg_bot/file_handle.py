import hashlib
import logging
from aiofiles import os

from io import BytesIO
from telegram import Update
from telegram.ext import CallbackContext


from core.crud import (
    create_file,
    get_user_all_file_paths_names,
    file_exists_in_database,
    get_file_by_filepath,
)
from tg_bot.kml_eng.merge import merge_kml_files_v2
from tg_bot.decorators import require_registration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MERGED_FILE_PATH = "./files/merged.kml"
COPY_STR = "_copy"


def calculate_file_hash(file_stream) -> str:
    hash_func = hashlib.sha256()
    for chunk in iter(lambda: file_stream.read(4096), b""):
        hash_func.update(chunk)
    return hash_func.hexdigest()


@require_registration
async def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file_name = document.file_name

    if document.mime_type != 'application/vnd.google-earth.kml+xml':
        await update.message.reply_text("Пожалуйста, отправьте KML файл.")
        return
    file = await document.get_file()
    file_stream = await file.download_as_bytearray()
    file_stream_io = BytesIO(file_stream)
    hash_value = calculate_file_hash(file_stream_io)
    file_stream_io.seek(0)
    path_to_file = f"./files/{hash_value[-16:]}"
    file_data = {
        "filehash": str(hash_value),
        "filename": str(file_name),
        "filepath": path_to_file,
        "created_by": int(update.message.from_user.id)
    }
    file_in_database = await file_exists_in_database(hash_value)
    file_in_store = False
    if file_in_database:
        file_in_store = await os.path.exists(file_in_database)
    else:
        file_in_store = await os.path.exists(path_to_file)
    if file_in_database and file_in_store:
        await update.message.reply_text(
            "Такой файл уже есть."
        )
        return
    if file_in_database:
        with open(file_in_database, "wb") as f:
            f.write(file_stream_io.read())
        await update.message.reply_text(
            "Файл по какойто причине отсутвовал в хранилище!\n"
            "Файл успешно записан на диск!\n"
            "Админу сообщил.")
        return
    if file_in_store:
        logger.warning(
            f"Файл {path_to_file} был в хранилище, но отсутвовал в бд!"
        )
        file_data["filepath"] = path_to_file + COPY_STR
        if await create_file(file_data):
            await update.message.reply_text("Ваш файл сохранен.")
        else:
            await update.message.reply_text(
                "Произошла ошибка при сохранении файла."
            )
        return
    with open(path_to_file, "wb") as f:
        f.write(file_stream_io.read())
    if await create_file(file_data):
        await update.message.reply_text("Ваш файл сохранен.")
    else:
        await update.message.reply_text(
            "Произошла ошибка при сохранении файла."
        )


async def check_file_paths(
    filepaths: list[tuple[str, str]]
) -> tuple[list[str], list[str]]:
    missing_files = []

    for path, name in filepaths:
        if not await os.path.exists(path):
            missing_files.append(path)
    return missing_files


@require_registration
async def get_my_merged_kml(update: Update, context: CallbackContext) -> None:
    """
    Отправляет пользователю файл 'merged.kml'.

    :param update: Объект обновления Telegram.
    :param context: Контекст обратного вызова.
    """

    filepaths_names = await get_user_all_file_paths_names(
        update.message.from_user.id)
    if not filepaths_names:
        await update.message.reply_text(
            "Ваших файлов у меня пока нету."
        )
        return
    missing_files = await check_file_paths(filepaths_names)
    if missing_files:
        filenames = []
        for filepath in missing_files:
            filenames.append(
                await get_file_by_filepath(filepath)
            )
        logger.info(
            f"Этих файлов нету!: {filenames}"
        )
        await update.message.reply_text(
            "Произошла ужасная ошибка: \n"
            f"Этих файлов нету!: {filenames}"
        )
        return
    my_merged = merge_kml_files_v2(filepaths_names)

    try:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=my_merged,
            filename="my_merged.kml"
        )
    except FileNotFoundError:
        await update.message.reply_text("Файл не найден.")
    except Exception as e:
        await update.message.reply_text(
            f"Произошла ошибка при отправке файла: {e}"
        )
    finally:
        my_merged.close()
