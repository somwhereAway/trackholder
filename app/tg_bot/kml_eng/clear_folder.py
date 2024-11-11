import os
import shutil


def clear_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не существует.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Не удалось удалить {file_path}. Причина: {e}")

    print(f"Папка {folder_path} очищена.")
