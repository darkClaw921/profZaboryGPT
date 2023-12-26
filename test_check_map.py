import folium

# координаты центра карты
center = [55.752923, 37.618871]

# создаем карту
m = folium.Map(location=center, zoom_start=10)

# добавляем геоточки на карту
def create_check_map(points:list):
    # points = [[37.222928, 55.765281], [37.222875, 55.76548]]  # замените точки на ваши
    # for point in points:
# /        folium.Marker(location=[point[1], point[0]]).add_to(m)
        # folium.Marker(location=[point[0], point[1]]).add_to(m)
    a = [(point[0], point[1]) for point in points]
    folium.PolyLine(a, tooltip="Coast").add_to(m)
    # сохраняем карту в HTML файл
    m.save('map.html')

#     trail_coordinates = [
#     (-71.351871840295871, -73.655963711222626),
#     (-71.374144382613707, -73.719861619751498),
#     (-71.391042575973145, -73.784922248007007),
#     (-71.400964450973134, -73.851042243124397),
#     (-71.402411391077322, -74.050048183880477),
# ]

    