import os
import random
import simplekml


def generate_line(num_points_per_file, kml, index):
    ls = kml.newlinestring(name=f'A LineString_{index}')
    coords = []
    for p in range(num_points_per_file):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        height = random.uniform(0, 70000)
        coords.append((lat, lon, height))
    ls.coords = coords
    ls.extrude = 1
    ls.altitudemode = simplekml.AltitudeMode.relativetoground


def generate_points(num_points_per_file, kml, index):
    for p in range(num_points_per_file):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        height = random.uniform(0, 70000)
        kml.newpoint(name=f"Point_{index}_{p}", coords=[(lon, lat, height)])


def generate_kml_files(output_folder, num_files, num_points_per_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    functions = [generate_line, generate_points]
    for i in range(num_files):
        kml = simplekml.Kml()
        function = random.choice(functions)
        function(num_points_per_file, kml, i)
        output_path = os.path.join(output_folder, f'file_{i + 1}.kml')
        kml.save(output_path)
        print(f"KML файл сохранен: {output_path}")
