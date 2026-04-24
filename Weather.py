import requests

address = "Spokane"
coords = requests.get(f"https://geocode.maps.co/search?q={address}&api_key=684b71249a52d829766865xau8d1b4e")
coords = coords.json()

lat = 47.658779
lon = -117.426048

weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
weather = weather.json()

temp = weather["current"]["temperature_2m"]
temp = temp*9/5 + 32

print(temp)