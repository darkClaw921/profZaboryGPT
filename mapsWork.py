# import requests
# import json

# # координаты начальной и конечной точек
# origin = "55.751244,37.618423"  # Москва
# destination = "59.938630,30.314130"  # Санкт-Петербург

# # запрос к API Directions
# url = f"https://api-maps.yandex.ru/services/route/2.0/?origin={origin}&destination={destination}&lang=ru-RU&apikey=9b9eb94f-3090-47fc-9fad-43133dfc9d83"
# response = requests.get(url)
# data = json.loads(response.content)
# print(data)
# # получение растояния маршрута
# distance = data["routes"][0]["distance"]
# print(f"Расстояние маршрута: {distance} метров")
import requests
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
GEOPOINT_BASE = '56.121457,37.895073'
# GEOPOINT_BASE = '37.895073,56.121457'



def get_geopoint(adress:str="липецк каменный лог 48"):

    # adress = "липецк каменный лог 48"
    reqUrl = f"https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API}&geocode={adress}&format=json"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    response = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    pprint(response.replace(' ',','))
    return response.replace(' ',',')

def get_distance(pointStar:str,pointEnd:str):
    # pointStar = "25.234369457896325,55.280222457968712"
    # pointEnd = "25.234369457896325,55.401544758961258"

    reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd}&avoid_tolls=true&mode=truck&apikey={MATRIX_API}"
    print(reqUrl)
    response = requests.get(reqUrl)
    data = response.json()
    pprint(data)
    status = data['route']['legs'][0]['status'] # ok
    
    steps= data["route"]['legs'][0]['steps']
    distance = 0
    duration = 0
    points = ''
    for step in steps:
        distance += step['length']
        duration += step['duration']

        
        for point in step['polyline']['points']:
            points += f"{point[1]},{point[0]},"
            break
        
    
    print(f"Расстояние маршрута: {distance} метров")
    print(f"Расстояние маршрута: {distance/1000} км")

    print(f"Время маршрута: {duration} секунд")
    print(f"Время маршрута: {duration/60} минут")


    
    return distance, points[:-1]


def get_static_map(points:str):
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    GEOPOINT_BASE_revers = '37.895073,56.121457'
    pointEnd_revers = '39.599229,52.608826'
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={GEOPOINT_BASE}&pt={GEOPOINT_BASE},pm2am~39.599229,52.608826,pm2bm&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    #TODO использовать uri для посторения точного маршрута
    reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pt={GEOPOINT_BASE},pm2am~{pointEnd_revers},pm2bm&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d" 
    
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pt={points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    print(reqUrl)
    response = requests.get(reqUrl)
    data = response.text
    # pprint(data)

# pointEnd = '39.580553,52.610494' #каменный лог
pointEnd = '52.608826,39.599229' #Липецк
# pointEnd = '39.599229,52.608826' #Липецк
# pointEnd = '56.121457,37.895073' #что-то от заказчика



# pointEnd = '56.097870, 37.886321'

distanse, points = get_distance(GEOPOINT_BASE,pointEnd)
get_static_map(points)
# get_geopoint()

