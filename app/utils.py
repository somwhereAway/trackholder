from pathlib import Path
from fuzzywuzzy import fuzz


def get_all_files_from_folder(folder: str) -> list[str]:
    """
    Получает список всех файлов из указанной папки, включая поддиректории.

    :param folder: Путь к папке.
    :return: Список строк с путями ко всем файлам.
    """
    path = Path(folder)
    return [str(file) for file in path.rglob('*') if file.is_file()]


def find_simillarity(user_query: str, correct_name: str) -> int:
    """
    Вычисляет степень сходства между двумя строками `user_query` и `correct_name` с помощью метрики Левенштейна, 
    возвращая процентное значение, указывающее на их схожесть.

    Параметры:
    - user_query (str): Введенная пользователем строка, которую нужно сравнить.
    - correct_name (str): Правильное название, с которым производится сравнение.

    Возвращает:
    - int: Значение от 0 до 100, представляющее процентное сходство между двумя строками. 
           Чем выше значение, тем более схожи строки.
    """
    return fuzz.ratio(correct_name.lower(), user_query.lower())
