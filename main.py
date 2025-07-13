import requests
import json
import csv
from staticmap import StaticMap, IconMarker
from PIL import Image
from google.transit import gtfs_realtime_pb2
from data.constants import *

def format_delay(seconds):
    rounded = round(seconds / 30) * 30
    if rounded == 0:
        return "zgodnie z rozkładem jazdy"
    minutes = rounded // 60
    remainder = rounded % 60
    return f"z opóźnieniem {minutes}:{remainder:02d} min"

def get_departures_by_name(stop_name):
    url = "https://www.peka.poznan.pl/vm/method.vm"
    data = {
        'method': 'getTimesForAllBollards',
        'p0': json.dumps({"name": stop_name})
    }

    response = requests.post(url, data=data)

    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text

def get_bus_by_vid(vid):
    response = requests.get(gtfs_rt_url)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            bus_data = entity.vehicle
            if bus_data.vehicle.id == vid:
                latitude = bus_data.position.latitude  # pozycja
                longitude = bus_data.position.longitude  # pozycja
                trip_id_rt = bus_data.trip.trip_id  # id kierunku
                current_stop_seq = bus_data.current_stop_sequence  # numer przystanku
                stop_headsign = None  # kierunek
                route_id = bus_data.trip.route_id  # linia
                schedule = bus_data.vehicle.label  # brygadówka

                print(latitude, longitude, trip_id_rt, stop_headsign, route_id, schedule)

        elif entity.HasField('trip_update'):
            trip_update = entity.trip_update
            if trip_update.vehicle.id == vid:
                for stu in trip_update.stop_time_update:
                    if stu.HasField("arrival") and stu.arrival.HasField("delay"):
                        delay = stu.arrival.delay
                        delay_str = format_delay(delay)

    with open("data/stop_times.txt", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row["trip_id"] == trip_id_rt and int(row["stop_sequence"]) == current_stop_seq:
                stop_headsign = row["stop_headsign"]
                arr_time = row["arrival_time"]
                dep_time = row["departure_time"]
                stop_id = row["stop_id"]
                break

    with open("data/stops.txt", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row["stop_id"] == stop_id:
                stop_code = row["stop_code"]
                stop_name = row["stop_name"]
                zone = row["zone_id"]
                break

    print(arr_time, dep_time, stop_id)
    print(f' Pojazd o numerze taborowym #{vid}, znajduje się na koordynatach {latitude}, {longitude}\n',
          f'Porusza się na linii: {schedule} w kierunku {stop_headsign}\n', 
          f'Zmierza na przystanek {stop_name}({stop_code}) w strefie {zone} {delay_str}')
    
    return latitude, longitude

latitude, longitude = get_bus_by_vid('1856')

m = StaticMap(512, 256)
icon = Image.open('data/img/poznan/bus.png')
icon_resized = icon.resize((46, 46), Image.Resampling.LANCZOS)
icon_resized.save('data/img/poznan/bus_res.png')
icon_marker = IconMarker((longitude, latitude), 'data/img/poznan/bus_res.png', 22, 22)  
m.add_marker(icon_marker)
image = m.render(zoom=16)
image.save('map.png')
