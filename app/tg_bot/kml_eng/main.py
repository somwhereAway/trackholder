import multiprocessing
from datetime import datetime

import clear_folder
import generte_random

# output_folder = "kml_files"
# clear_folder.clear_folder(output_folder)
#
# num_files = 100
# num_points_per_file = 10000
# generte_random.generate_kml_files(
#     output_folder, num_files, num_points_per_file)
#
if __name__ == '__main__':
    print('Начало работы основного потока')
    start_time = datetime.now()
    end_time = datetime.now()
    print('Окончание работы основного потока')
    print(f'Итоговое время выполнения: {end_time - start_time} секунд.')
