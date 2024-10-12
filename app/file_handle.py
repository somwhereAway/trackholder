import hashlib

from telegram import Update
from telegram.ext import CallbackContext

from io import BytesIO

from app.crud import create_file, get_all_files


def calculate_file_hash(file_stream) -> str:
    hash_func = hashlib.sha256()  # Можно заменить на md5 или другой алгоритм
    for chunk in iter(lambda: file_stream.read(4096), b""):
        hash_func.update(chunk)
    return hash_func.hexdigest()


async def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file_name = document.file_name
    if document.mime_type == 'application/vnd.google-earth.kml+xml':
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
        }
        if await create_file(file_data):
            with open(path_to_file, "wb") as f:
                f.write(file_stream_io.read())
            await update.message.reply_text(f"Хэш-сумма файла: {hash_value}")
        else:
            await update.message.reply_text("Этот файл есть в базе данных")
    else:
        await update.message.reply_text("Пожалуйста, отправьте KML файл.")


async def show_all_files(update: Update, context: CallbackContext) -> None:
    files = await get_all_files()
    for file in files:
        print(file.filehash)
