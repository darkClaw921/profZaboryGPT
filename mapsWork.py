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

AVOID_ZONE='55.729772,37.620528|55.752637,37.583323|55.773591,37.621260|55.750507,37.656021'
def download_map(url:str):
    response = requests.get(url)
    data = response.content
    with open("map.png", "wb") as file:
        file.write(data)
    return data


def get_geopoint(adress:str="липецк"):

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

    print(pointEnd_revers)
    print(pointEnd)
    # reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd}&avoid_tolls=true&mode=truck&apikey={MATRIX_API}" 
    reqUrl = f"https://api.routing.yandex.net/v2/route?waypoints={pointStar}|{pointEnd_revers}&avoid_zones={AVOID_ZONE}&avoid_tolls=true&mode=truck&apikey={MATRIX_API}"
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
    
    # pointEnd = pointEnd.split(',') 
    # pointEnd_revers = f"{pointEnd[1]},{pointEnd[0]}"# '39.599229,52.608826'
    # pointEnd_revers = pointEnd
    #TODO использовать uri для посторения точного маршрута
    reqUrl = f"https://static-maps.yandex.ru/v1?lang=ru_RU&pt={GEOPOINT_BASE_revers},pm2am~{pointEnd},pm2bm&pl=c:8822DDC0,w:5,{points}&apikey={STATIC_API}" 
    
    print(reqUrl)
    response = requests.get(reqUrl)
    data = response.text
    # mapPath = download_map(reqUrl)
    # return mapPath
    return reqUrl
    # pprint(data)

def get_more_adress(adress:str):
    url = f"https://suggest-maps.yandex.ru/v1/suggest?apikey={GEOADREDS_API}&text={adress}&lang=ru_RU"
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


def main():
    adress='липецк'
    pointEnd = get_geopoint(adress=adress)
    distanse, points = get_distance(GEOPOINT_BASE_revers ,pointEnd)
    mapPath = get_static_map(points,pointEnd)
    return mapPath, distanse

def get_map(adress:str)->list:
    """Путь до картинки и расстояние"""
    pointEnd = get_geopoint(adress=adress)
    pointStart = GEOPOINT_BASE
    
    
    distanse, points = get_distance(pointStart,pointEnd)
    mapPath = get_static_map(points,pointEnd)
    return mapPath, distanse


# distanse, points = get_distance(GEOPOINT_BASE,pointEnd)
# mapPath = get_static_map(points,pointEnd)
# get_map('Московская область, красногорск')
# get_map('Липецк')
# print(quests)
# get_geopoint()

