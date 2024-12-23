import osmnx as ox
from geopy.distance import geodesic
from datetime import datetime
import requests

# Константы
SPEED_THRESHOLD = 10  # км/ч для определения пешеходного движения
API_OSM_NODES_URL = "https://nominatim.openstreetmap.org/reverse"


def calculate_speed(prev_point, current_point, prev_time, current_time):
    """Расчет скорости между двумя точками."""
    distance = geodesic(prev_point, current_point).kilometers
    time_delta = (current_time - prev_time).total_seconds() / \
        3600  # время в часах
    if time_delta == 0:  # избежать деления на 0
        return 0
    return distance / time_delta


def get_area_info(lat, lon):
    """Использует OSM API для получения информации о местности (например, тип дороги и населенный пункт)."""
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'addressdetails': 1,
        'zoom': 18
    }

    response = requests.get(API_OSM_NODES_URL, params=params)
    data = response.json()

    # Проверим, находится ли точка в населенном пункте
    if 'address' in data and 'town' in data['address']:
        return 'urban'  # Населенный пункт
    elif 'highway' in data['tags'] and data['tags']['highway'] in ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']:
        return 'asphalt_road'  # Асфальтированная дорога
    else:
        return 'rural'  # Грунтовая дорога или природная местность


def filter_track_by_speed_and_road_type(track_points):
    """Фильтрует трек, оставляя только участки, пройденные пешком вне асфальтированных дорог и вне населенных пунктов."""
    filtered_track = []
    prev_point = None
    prev_time = None

    for point in track_points:
        current_point = (point['lat'], point['lon'])
        current_time = datetime.fromisoformat(point['timestamp'])

        # Определение типа местности для текущих координат
        area_type = get_area_info(point['lat'], point['lon'])

        # Если есть предыдущая точка, вычисляем скорость
        if prev_point and prev_time:
            speed = calculate_speed(
                prev_point, current_point, prev_time, current_time)

            # Если скорость меньше порога и местность не асфальтированная дорога или населенный пункт
            if speed <= SPEED_THRESHOLD and area_type != 'asphalt_road' and area_type != 'urban':
                filtered_track.append(point)
        else:
            # Добавляем первую точку, так как у нее нет предыдущей
            filtered_track.append(point)

        # Обновляем предыдущую точку и время
        prev_point = current_point
        prev_time = current_time

    return filtered_track


# Пример использования
track_points = [
    {'lat': 55.7558, 'lon': 37.6173, 'timestamp': '2024-12-23T12:00:00'},
    {'lat': 55.7560, 'lon': 37.6175, 'timestamp': '2024-12-23T12:05:00'},
    {'lat': 55.7565, 'lon': 37.6180, 'timestamp': '2024-12-23T12:10:00'},
    {'lat': 55.7580, 'lon': 37.6200, 'timestamp': '2024-12-23T12:15:00'},
    {'lat': 55.7600, 'lon': 37.6250, 'timestamp': '2024-12-23T12:20:00'},
]

filtered_track = filter_track_by_speed_and_road_type(track_points)
print(filtered_track)
