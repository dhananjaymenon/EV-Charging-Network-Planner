import json
import polyline
from urllib.parse import urlencode
import APIKey
import requests

api_key = APIKey.api_key

class Place:
    def __init__(self,name,location,ba_rating,rating,num_of_ratings):
        self.name = name
        self.location = location
        self.ba_rating = ba_rating
        self.rating = rating
        self.num_of_ratings = num_of_ratings


def find_sum(List):
    sum=0.0
    for i in List:
        sum+=i
    return sum

def HMS(seconds):
    hrs = int(seconds / 3600)
    min = int((seconds % 3600) / 60)
    sec = int(seconds % 60)
    time = []
    time.append(hrs)
    time.append(min)
    time.append(sec)
    return time

def frame_splitter(frame_number):
    for i in range(frame_number+1):
        if ((i + i + 1)==frame_number+1):
            return i

def extractGeoJSON(coordinate_list):
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

    way_points[-1] = coordinate_list[-1]

    Result = []
    Result.append(all_points)
    Result.append(way_points)
    return Result

def path_splitter(path,coordinate1,coordinate2):
    split_point_1 = 0
    split_point_2 = 0
    for i in path:
        if(round(i[0],2)==round(coordinate1[0],2) and round(i[1],2)==round(coordinate1[1],2)):
            split_point_1 = path.index(i)
        if(round(i[0],2)==round(coordinate2[0],2) and round(i[1],2)==round(coordinate2[1],2)):
            split_point_2 = path.index(i)
    path_1 = path[:split_point_1]
    path_2 = path[split_point_1:split_point_2]
    path_3 = path[split_point_2:]
    paths = []
    paths.append(path_1)
    paths.append(path_2)
    paths.append(path_3)
    return paths

def nearby_places_url(location,time_sec,place_types):
    avg_walking_speed = 1.42  # metres per second
    if(time_sec<1200):
        time_sec = 1200
    radius = (time_sec*avg_walking_speed)/2
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    type_string = ",".join(place_types)

    params = {
        "location":f"{location[0]},{location[1]}",
        "radius":radius,
        "type":type_string,
        "key":api_key
    }
    params_encoded = urlencode(params)
    places_url = f"{endpoint}?{params_encoded}"
    print(radius)
    #print(places_url)
    return places_url

def bayesian_average(product_ratings_average,product_ratings_count):
    m = 3
    C = 25
    b_a = (product_ratings_average*product_ratings_count + m*C) / (product_ratings_count + C)
    return b_a

def JSON_to_placeList(filename):
    places = []
    file = open(filename,encoding="utf8")
    jdata = file.read()
    jobj = json.loads(jdata)

    results = jobj['results']

    for result in results:
        name = result['name']
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        loc = []
        avg_rating = -1
        rating_count = -1
        ba_rating = -1
        if ('rating' in result):
            avg_rating = result['rating']
            rating_count = result['user_ratings_total']
            ba_rating = bayesian_average(avg_rating, rating_count)
        loc.append(lat)
        loc.append(lng)
        places.append(Place(name,loc,ba_rating,avg_rating,rating_count))

    for i in range(len(places)-1,0,-1):
        for j in range(i):
            if(places[j].ba_rating < places[j+1].ba_rating):
                temp = places[j]
                places[j] = places[j+1]
                places[j+1] = temp

    return places

def walking_route(origin,destination,file_location):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    origin_string = f"{origin[0]},{origin[1]}"
    destination_string = f"{destination[0]},{destination[1]}"

    params = {
        "origin": origin_string,
        "destination": destination_string,
        "mode": "walking",
        "key": api_key
    }
    params_encoded = urlencode(params)
    places_url = f"{endpoint}?{params_encoded}"

    json_data = requests.get(places_url).json()

    with open(file_location, 'w') as json_file:
        json.dump(json_data, json_file)

    #WRITING PATH
    all_points = []
    file = open('NA/directions.json', encoding="utf8")
    jdata = file.read()
    jobj = json.loads(jdata)

    legs = jobj['routes'][0]['legs']
    for leg in legs:
        steps = leg['steps']
        for step in steps:
            polyline_string = step['polyline']['points']
            points = polyline.decode(polyline_string)
            all_points.extend(points)

    return all_points
