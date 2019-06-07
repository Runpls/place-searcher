#!/usr/bin/env python3
import requests
import time
import json

api_url_base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
location_coordinates = "10.8042943,106.7140793"
radius = 2000
keyword = 'quán bia'


def get_api_key():
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close
    return api_key


def nearby_search(location, radius, keyword):
    api_key = get_api_key()
    places = []
    params = {
        'location': location,
        'radius': radius,
        'keyword': keyword,
        'key': api_key
    }
    with requests.session() as sess:
        response = sess.get(api_url_base, params=params)
        if response.status_code == 200:
            data = response.json()
            places.extend(data['results'])
            time.sleep(2)
            while 'next_page_token' in data:
                params['pagetoken'] = data['next_page_token'],
                response = sess.get(api_url_base, params=params)
                data = response.json()
                places.extend(data['results'])
                time.sleep(2)
            return places
        else:
            print('[!] HTTP {0} calling [{1}]'.format(
                response.status_code, api_url_base))
            return None


def write_GeoJSON(data_google_map):
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [data["geometry"]["location"]["lng"],
                                    data["geometry"]["location"]["lat"]],
                },
                "properties": {
                    "name": data["name"],
                    "address": data["vicinity"],
                    "rating": data["rating"]
                },
            } for data in data_google_map]
    }
    with open('map.geojson', 'wt') as f:
        json.dump(geojson, f, indent=4)


def main():
    data_google_map = nearby_search(location_coordinates, radius, keyword)
    write_GeoJSON(data_google_map)


if __name__ == "__main__":
    main()
