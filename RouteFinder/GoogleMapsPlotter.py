import googlemaps
import requests
import json
from urllib.parse import urlencode, urlparse, parse_qsl

import polyline
import gmplot
import webbrowser

##INSERT YOUR API KEY HERE##
import APIKey
api_key = APIKey.api_key
## ##

def ret_lat_lng(List):
    lat = []
    lng = []
    R = []
    for x in List:
        lat.append(x[0])
        lng.append(x[1])
    R.append(lat)
    R.append(lng)
    return R


class GoogleMapsPlotter:

    def __init__(self,coordinate_list, avoid_tolls = False, avoid_highways = False):
        self.coordinate_list = coordinate_list
        self.avoid_tolls = avoid_tolls
        self.avoid_highways = avoid_highways

    def extractGeoJSON(self):
        all_points = []
        way_points = []

        file = open('GMP/directions.json', encoding="utf8")
        jdata = file.read()
        jobj = json.loads(jdata)

        legs = jobj['routes'][0]['legs']
        for leg in legs:
            steps = leg['steps']
            start = 0
            for step in steps:
                polyline_string = step['polyline']['points']
                points = polyline.decode(polyline_string)
                all_points.extend(points)
                if (start == 0):
                    way_points.append(points[0])
                    start = 1

        way_points[-1] = self.coordinate_list[-1]

        Result = []
        Result.append(all_points)
        Result.append(way_points)
        return Result

    def return_center(self):
        x=0.0
        y=0.0
        for i in self.coordinate_list:
            x+=i[0]
            y+=i[1]
        x = x/len(self.coordinate_list)
        y = y/len(self.coordinate_list)
        return [x,y]

    def List2GeoJSON(self):
        List = self.coordinate_list
        avoid_tolls = self.avoid_tolls
        avoid_highways = self.avoid_highways
        avoid_string = "ferries,indoor"
        if (avoid_tolls):
            avoid_string = avoid_string + ",tolls"
        if (avoid_highways):
            avoid_string = avoid_string + ",highways"

        endpoint = "https://maps.googleapis.com/maps/api/directions/json"
        if (len(List) == 2):
            origin = f"{List[0][0]},{List[0][1]}"
            destination = f"{List[1][0]},{List[1][1]}"

        else:
            last_ele = len(List) - 1
            origin = f"{List[0][0]},{List[0][1]}"
            destination = f"{List[last_ele][0]},{List[last_ele][1]}"
            waypoints_string = ""
            for i in range(1, last_ele):
                waypoints_string += f"{List[i][0]},{List[i][1]}|"
            waypoints_string += f"{List[last_ele - 1][0]},{List[last_ele - 1][1]}"

        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints_string,
            "mode": "driving",
            "avoid": avoid_string,
            "key": api_key
        }
        params_encoded = urlencode(params)
        places_url = f"{endpoint}?{params_encoded}"

        json_data = requests.get(places_url).json()
        with open('GMP/directions.json','w') as json_file:
            json.dump(json_data,json_file)

    def GeoJSON2html(self):
        all_points = []
        way_points = []

        file = open('GMP/directions.json', encoding="utf8")
        jdata = file.read()
        jobj = json.loads(jdata)

        legs = jobj['routes'][0]['legs']
        for leg in legs:
            steps = leg['steps']
            start = 0
            for step in steps:
                polyline_string = step['polyline']['points']
                points = polyline.decode(polyline_string)
                all_points.extend(points)
                if (start == 0):
                    way_points.append(points[0])
                    start = 1

        file.close()

        R = ret_lat_lng(all_points)
        lat = R[0]
        lng = R[1]

        WP = ret_lat_lng(way_points)
        lat_ps = WP[0]
        lng_ps = WP[1]

        gmapPlot = gmplot.GoogleMapPlotter(lat[0], lng[1], 10, apikey=api_key)
        gmapPlot.scatter(lat_ps, lng_ps, '#ff000', size=50, marker=True)
        gmapPlot.plot(lat, lng, 'blue', edge_width=2.5)
        gmapPlot.draw("GMP/map.html")
        #webbrowser.open_new_tab("GMP/map.html")

    def MapPlotter(self):
        self.List2GeoJSON()
        self.GeoJSON2html()
