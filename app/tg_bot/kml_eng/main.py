import multiprocessing
import os
from datetime import datetime

import clear_folder
import generate_random
import merge


if __name__ == '__main__':
    output_folder = "kml_files"
    clear_folder.clear_folder(output_folder)
    num_files = 100
    num_points_per_file = 1000
    generate_random.generate_kml_files(
        output_folder, num_files, num_points_per_file)
    start_time = datetime.now()
    files = [os.path.join(output_folder, f) for f in os.listdir(
        output_folder) if os.path.isfile(os.path.join(output_folder, f))]
    merge.merge_kml_filesv2(files)
    end_time = datetime.now()
    print('Окончание работы основного потока')
    print(f'Итоговое время выполнения: {end_time - start_time} секунд.')
    clear_folder.clear_folder(output_folder)
