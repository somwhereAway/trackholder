from pathlib import Path


def get_all_files_from_folder(folder: str) -> list[str]:
    """
    Получает список всех файлов из указанной папки, включая поддиректории.

    :param folder: Путь к папке.
    :return: Список строк с путями ко всем файлам.
    """
    path = Path(folder)
    return [str(file) for file in path.rglob('*') if file.is_file()]
