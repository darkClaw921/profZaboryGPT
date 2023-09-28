import requests
import json

# координаты начальной и конечной точек
origin = "55.751244,37.618423"  # Москва
destination = "59.938630,30.314130"  # Санкт-Петербург

# запрос к API Directions
url = f"https://api-maps.yandex.ru/services/route/2.0/?origin={origin}&destination={destination}&lang=ru-RU&apikey=9b9eb94f-3090-47fc-9fad-43133dfc9d83"
response = requests.get(url)
data = json.loads(response.content)
print(data)
# получение растояния маршрута
distance = data["routes"][0]["distance"]
print(f"Расстояние маршрута: {distance} метров")