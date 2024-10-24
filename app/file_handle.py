import hashlib

from io import BytesIO
from telegram import Update
from telegram.ext import CallbackContext


from app.crud import create_file, get_user_all_file_paths
from app.kml_utils import merge_kml_files_parallel


MERGED_FILE_PATH = "./files/merged.kml"


def calculate_file_hash(file_stream) -> str:
    hash_func = hashlib.sha256()  # Можно заменить на md5 или другой алгоритм
    for chunk in iter(lambda: file_stream.read(4096), b""):
        hash_func.update(chunk)
    return hash_func.hexdigest()


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
    path_to_file = f"./files/{hash_value[-10:]}"
    file_data = {
        "filehash": str(hash_value),
        "filename": str(file_name),
        "filepath": str(path_to_file),
        "created_by": int(update.message.from_user.id)
    }
    if await create_file(file_data):
        with open(path_to_file, "wb") as f:
            f.write(file_stream_io.read())
        await update.message.reply_text("Ваш файл сохранен.")
    else:
        await update.message.reply_text("Этот файл есть в базе данных")


async def get_my_merged_kml(update: Update, context: CallbackContext) -> None:
    """
    Отправляет пользователю файл 'merged.kml'.

    :param update: Объект обновления Telegram.
    :param context: Контекст обратного вызова.
    """
    filepaths = await get_user_all_file_paths(update.message.from_user.id)
    my_merged = await merge_kml_files_parallel(filepaths)

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