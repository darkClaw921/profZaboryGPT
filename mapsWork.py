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
from typing import List
load_dotenv()
import os
from test_check_map import create_check_map
GEOPOINT_BASE_revers = '37.895073,56.121457'
GEOPOINT_BASE = '56.121457,37.895073'
# GEOPOINT_BASE = '37.895073,56.121457'
GEOCODER_API = os.environ.get('GEOCODER_API')
MATRIX_API = os.environ.get('MATRIX_API')
GEOADRES = os.environ.get('GEOADRES_API')
STATIC_API = os.environ.get('STATIC_API')


def download_map(url:str):
    # url = 'https://static-maps.yandex.ru/1.x/?lang=ru_RU&ll=37.895073,56.121457&pt=37.895073,56.121457,pm2am~39.599229,52.608826,pm2bm&pl=c:8822DDC0,w:5,37.895073,56.121457,39.599229,52.608826&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d'
    response = requests.get(url)
    data = response.content
    with open("map.png", "wb") as file:
        file.write(data)
    return data


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
    pointEnd = pointEnd.split(',') 
    pointEnd_revers = f"{pointEnd[1]},{pointEnd[0]}"# '39.599229,52.608826'
    # reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd}&avoid_tolls=true&mode=truck&apikey={MATRIX_API}"
    reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd_revers}&avoid_tolls=true&mode=truck&apikey={MATRIX_API}"
    # reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd}&avoid_tolls=true&mode=truck&weight=12&apikey={MATRIX_API}"
    print(reqUrl)
    response = requests.get(reqUrl)
    data = response.json()
    # pprint(data)
    status = data['route']['legs'][0]['status'] # ok
    if status == 'FAIL':
        pprint(data)
    steps= data["route"]['legs'][0]['steps']
    distance = 0
    duration = 0
    points = ''
    allPoint =[]
    for step in steps:
        distance += step['length']
        duration += step['duration']

        
        lenStep = len(step['polyline']['points'])
        lenStep = lenStep//2
        
        # for point in step['polyline']['points']:
        #     # points += f"{point[1]},{point[0]},"
        #     points += f"{point[0]},{point[1]},"
        #     # points += f"{point[0]},{point[1]},"
        #     break
        point = step['polyline']['points'][0]
        points += f"{point[1]},{point[0]},"
        # points += f"{point[0]},{point[1]},"

        point = step['polyline']['points'][lenStep]
        points += f"{point[1]},{point[0]},"
        # points += f"{point[0]},{point[1]},"

        point = step['polyline']['points'][-1]
        points += f"{point[1]},{point[0]},"
        # points += f"{point[0]},{point[1]},"
        
        allPoint.extend(step['polyline']['points'])

    create_check_map(allPoint)

    print(f"Расстояние маршрута: {distance} метров")
    print(f"Расстояние маршрута: {distance/1000} км")

    print(f"Время маршрута: {duration} секунд")
    print(f"Время маршрута: {duration/60} минут")


    distance = distance/1000 #км
    return round(distance), points[:-1]

def get_static_map(points:str,pointEnd:str):
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    
    # pointEnd = pointEnd.split(',') 
    # pointEnd_revers = f"{pointEnd[1]},{pointEnd[0]}"# '39.599229,52.608826'
    # pointEnd_revers = pointEnd
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={GEOPOINT_BASE_revers}&pt={GEOPOINT_BASE_revers},pm2am~37.319484,55.820369,pm2bm&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    #TODO использовать uri для посторения точного маршрута
    reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pt={GEOPOINT_BASE_revers},pm2am~{pointEnd},pm2bm&pl=c:8822DDC0,w:5,{points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d" 
    
    # reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pt={points}&apikey=bdd5228a-b658-4665-a381-d9cbc4e27a2d"
    print(reqUrl)
    response = requests.get(reqUrl)
    data = response.text
    # mapPath = download_map(reqUrl)
    # return mapPath
    return reqUrl
    # pprint(data)

def get_more_adress(adress:str):
    url = f"https://suggest-maps.yandex.ru/v1/suggest?apikey=08bc34bd-ed3f-4441-b670-071bdcae068d&text={adress}&lang=ru_RU"
    response = requests.get(url)
    data = response.json()
    pprint(data)
    adress = data['results']
    adresDict= {}
    for i, adres in enumerate(adress):
        try:
            adresDict[str(i)] = f"{adres['subtitle']['text']} {adres['title']['text']}"
        except:
            adresDict[str(i)] = f"{adres['title']['text']}"
        if i==2: break
    pprint(adresDict)
    return adresDict

# pointEnd = '39.580553,52.610494' #каменный лог
# pointEnd = '52.608826,39.599229' #Липецк
# pointEnd = '39.599229,52.608826' #Липецк
# pointEnd = '56.121457,37.895073' #что-то от заказчика

def main():
    adress='липецк каменный лог 48'
    pointEnd = get_geopoint(adress=adress)
    distanse, points = get_distance(GEOPOINT_BASE_revers ,pointEnd)
    mapPath = get_static_map(points,pointEnd)
    return mapPath, distanse

def get_map(adress:str)->list:
    """Путь до картинки и расстояние"""
    pointEnd = get_geopoint(adress=adress)
    pointStart = GEOPOINT_BASE
    # pointEnd = '37.319432,55.820375'
    # pointStart = '37.893685,56.120397'
    # pointEnd = '52.608826,39.599229'
    # pointEnd = '39.599229,52.608826'
    
    distanse, points = get_distance(pointStart,pointEnd)
    mapPath = get_static_map(points,pointEnd)
    return mapPath, distanse

# pointEnd = '56.097870, 37.886321'

# distanse, points = get_distance(GEOPOINT_BASE,pointEnd)
# mapPath = get_static_map(points,pointEnd)
# a = get_more_adress('каменный лог 48')
# get_map('Московская область, красногорск')
# get_map('Владимирская область, город Владимир')
# print(quests)
# get_geopoint()

