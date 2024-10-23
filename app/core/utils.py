import logging
import os

from pathlib import Path


def get_all_files_from_folder(folder: str) -> list[str]:
    """
    Получает список всех файлов из указанной папки, включая поддиректории.

    :param folder: Путь к папке.
    :return: Список строк с путями ко всем файлам.
    """
    path = Path(folder)
    return [str(file) for file in path.rglob('*') if file.is_file()]


logger = logging.getLogger(__name__)


def delete_file(path_to_file: str) -> None:
    """Удаляет файл.

    Args:
        path_to_file (_type_): путь к файлу
    """
    try:
        if os.path.exists(path_to_file):
            os.remove(path_to_file)
            logger.info(f"Файл {path_to_file} успешно удален.")
        else:
            logger.warning(f"Файл {path_to_file} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при удалении файла: {e}")
