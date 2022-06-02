import APIKey
import math
import requests
import json
import os
from geopy import distance
import numpy as np
from GoogleOptimalRoute import *
from urllib.parse import urlencode

json_holder_name = "JsonHolder"

def convertList2URL(CX,CY):
    url=""
    n = len(CX)
    for i in range(n):
        url = url+str(CX[i])+"%2C"
        url = url+str(CY[i])+"%7C"
    return url

def url_generator(CX,CY):
    CXkm = CX
    CYkm = CY
    num = len(CXkm)
    print(num)
    apikey = APIKey.api_key

    url_beginning = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    url_list = []
    url_key = "&key=" + apikey

    grid_num = math.ceil(float(num / 10))
    print(f'come on {grid_num}')

    for i in range(1, grid_num + 1):
        print(i)
        if (i == grid_num):
            mat_num = int(math.pow(i, 2) - math.pow(i - 1, 2))
            for k in range(1, mat_num + 1):

                if (k == i):
                    CXnew = CXkm[(grid_num - 1) * 10: num]
                    CYnew = CYkm[(grid_num - 1) * 10: num]
                    url_origins = convertList2URL(CXnew, CYnew)
                    url_destinations = convertList2URL(CXnew, CYnew)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)

                elif (k < i):
                    CXnew1 = CXkm[(k - 1) * 10: k * 10]
                    CYnew1 = CYkm[(k - 1) * 10: k * 10]
                    CXnew2 = CXkm[(grid_num - 1) * 10: num]
                    CYnew2 = CYkm[(grid_num - 1) * 10: num]
                    url_origins = convertList2URL(CXnew1, CYnew1)
                    url_destinations = convertList2URL(CXnew2, CYnew2)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)

                elif (k > i):
                    CXnew1 = CXkm[(grid_num - 1) * 10: num]
                    CYnew1 = CYkm[(grid_num - 1) * 10: num]
                    CXnew2 = CXkm[(mat_num - k) * 10: (mat_num - k + 1) * 10]
                    CYnew2 = CYkm[(mat_num - k) * 10: (mat_num - k + 1) * 10]
                    url_origins = convertList2URL(CXnew1, CYnew1)
                    url_destinations = convertList2URL(CXnew2, CYnew2)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)
        else:
            mat_num = int(math.pow(i, 2) - math.pow(i - 1, 2))
            for k in range(1, mat_num + 1):
                if (k == i):
                    CXnew = CXkm[(k - 1) * 10: k * 10]
                    CYnew = CYkm[(k - 1) * 10: k * 10]
                    url_origins = convertList2URL(CXnew, CYnew)
                    url_destinations = convertList2URL(CXnew, CYnew)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)

                elif (k < i):
                    print("Capital F")
                    CXnew1 = CXkm[(k - 1) * 10: k * 10]
                    CYnew1 = CYkm[(k - 1) * 10: k * 10]
                    CXnew2 = CXkm[(i - 1) * 10: i * 10]
                    CYnew2 = CYkm[(i - 1) * 10: i * 10]
                    url_origins = convertList2URL(CXnew1, CYnew1)
                    url_destinations = convertList2URL(CXnew2, CYnew2)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)

                elif (k > i):
                    CXnew1 = CXkm[(i - 1) * 10: i * 10]
                    CYnew1 = CYkm[(i - 1) * 10: i * 10]
                    CXnew2 = CXkm[(mat_num - k) * 10: (mat_num - k + 1) * 10]
                    CYnew2 = CYkm[(mat_num - k) * 10: (mat_num - k + 1) * 10]
                    url_origins = convertList2URL(CXnew1, CYnew1)
                    url_destinations = convertList2URL(CXnew2, CYnew2)
                    url_1 = "origins=" + url_origins
                    url_2 = "&destinations=" + url_destinations
                    url = url_beginning + url_1 + url_2 + url_key
                    url_list.append(url)

    for url in url_list:
        print(url)
    return url_list

def save_json_files(url_list):

    #DELETE CONTENTS OF DIRECTORY
    import os, shutil
    folder = json_holder_name
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    c=1
    for url_string in url_list:
        json_data = requests.get(url_string).json()

        with open(f'{json_holder_name}/Panel{c}.json','w') as json_file:
            json.dump(json_data, json_file)

        c = c + 1

def json_to_path(num,coor_list):
    DIR = json_holder_name
    #number_of_places = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    panel_num = int(math.pow(math.ceil(float(num / 10)), 2))
    print(panel_num)
    j_list = []

    for i in range(1, panel_num + 1):
        j = open(f'{json_holder_name}/Panel{i}.json')
        j_list.append(j)

    matrix_list = []
    counter = 0
    for j in j_list:
        counter += 1
        jdata = j.read()
        jobj = json.loads(jdata)

        rows = jobj['rows']
        n_rows = len(rows)
        matrix = []



        print(f"============Matrix {counter}============")

        for i in range(n_rows):
            elements = rows[i]['elements']
            n_col = len(elements)
            row = []
            for j in range(n_col):
                print(f"{elements[j]['distance']['value']:04}", end="\t")
                row.append(elements[j]['distance']['value'])
            matrix.append(row)
            print()
        print("=================================")
        matrix_list.append(matrix)

    # for i in matrix_list:
    # print(i)

    megamatrix = np.zeros((num, num), dtype=int)

    ##TRICK TILL 3x3
    col_c = [0, 10, 10, 0, 20, 20, 20, 10, 0, 30, 30, 30, 30, 20, 10, 0, 40, 40, 40, 40, 40, 30, 20, 10, 0]
    row_c = [0, 0, 10, 10, 0, 10, 20, 20, 20, 0, 10, 20, 30, 30, 30, 30, 0, 10, 20, 30, 40, 40, 40, 40, 40]

    for i in range(len(matrix_list)):

        for row in range(len(matrix_list[i])):

            for col in range(len(matrix_list[i][0])):
                megamatrix[row + row_c[i]][col + col_c[i]] = matrix_list[i][row][col]

    # print(megamatrix)
    matrix = megamatrix

    TSP_object = TSP(matrix)

    path_and_distance = TSP_object.return_solution()

    ##MAKE CHANGES - REMOVE LAST##

    print(path_and_distance[0])
    print(f"Total Distance : {path_and_distance[1] / 1000} km")

    optimal_path = path_and_distance[0]
    dist = path_and_distance[1]
    optimal_path.pop()

    ##CHANGES MADE##

    print(optimal_path)
    coor_path = []
    for i in optimal_path:
        coor_path.append(coor_list[i])
    ret_path_and_distance = []
    ret_path_and_distance.append(coor_path)
    ret_path_and_distance.append(dist)
    return ret_path_and_distance

def get_distance_and_time(origin,destination):
    api_key = APIKey.api_key
    origin_url = str(origin[0]) + "," + str(origin[1]) + "|"
    destination_url = str(destination[0]) + "," + str(destination[1]) + "|"
    data_type = "json"
    endpoint = f"https://maps.googleapis.com/maps/api/distancematrix/{data_type}"
    params = {"origins": origin_url, "destinations": destination_url, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    #print(url)
    r = requests.get(url)
    #print(r.json())
    print(r.json()['rows'][0]['elements'][0]['distance']['text'])
    dist = r.json()['rows'][0]['elements'][0]['distance']['value']
    distance_km = dist/1000
    time = r.json()['rows'][0]['elements'][0]['duration']['value']
    R = []
    #R.append(distance_km)
    R.append(dist)
    R.append(time)
    return R

##MORE

def generate_distancematrix(List):
    print(List)
    matrix = []
    for i in List:
        row = []
        for j in List:
            dist = distance.distance(i,j).km
            row.append(dist)
        matrix.append(row)
    return matrix

def array_shifter_end(List,index):
    length = len(List)
    ret_List = []
    ret_List.extend(List[(index+1)%length:])
    ret_List.extend(List[:(index+1)%length])
    return ret_List

def array_shifter_beginning(List,index):
    length = len(List)
    ret_List = []
    ret_List.extend(List[index % length:])
    ret_List.extend(List[:index % length])
    return ret_List

def array_reverse(List):
    return List[::-1]

def connector(path_list,distance_list):
    #blob = path_list[0]
    blob = []
    distance_increase = 0
    distance_decrease = 0

    for path in path_list:
        if(len(blob)==0):
            blob.extend(path)
            continue
        dist = float('inf')
        pointer_A = 0
        pointer_B = 0
        for A in range(len(blob)):
            for B in range(len(path)):
                gpd = distance.distance(blob[A], path[B]) + \
                      distance.distance(blob[(A + 1) % len(blob)], path[(B - 1) % len(path)])

                if (gpd < dist):
                    dist = gpd
                    pointer_A = A
                    pointer_B = B

        distance_increase += get_distance_and_time(blob[pointer_A], path[pointer_B])[0]
        distance_increase += get_distance_and_time(path[(pointer_B-1) % len(path)], blob[(pointer_A+1) % len(blob)])[0]
        distance_decrease += get_distance_and_time(blob[pointer_A], blob[(pointer_A+1) % len(blob)])[0]
        distance_decrease += get_distance_and_time(path[(pointer_B-1) % len(path)], path[pointer_B])[0]
        print("---------------------")
        print("---------IMP---------")
        print("INCREASE")
        print(blob[pointer_A],path[pointer_B],get_distance_and_time(blob[pointer_A], path[pointer_B])[0])
        print(path[(pointer_B-1) % len(path)], blob[(pointer_A+1) % len(blob)], get_distance_and_time(path[(pointer_B-1) % len(path)], blob[(pointer_A+1) % len(blob)])[0])
        print("DECREASE")
        print(blob[pointer_A],blob[(pointer_A+1)%len(blob)],get_distance_and_time(blob[pointer_A], blob[(pointer_A+1) % len(blob)])[0])
        print(path[(pointer_B-1)%len(path)],path[pointer_B],get_distance_and_time(path[(pointer_B-1) % len(path)], path[pointer_B])[0])

        segment1 = array_shifter_end(blob,pointer_A)
        #path_reverse = array_reverse(path)
        segment2 = array_shifter_beginning(path,pointer_B)
        blob = segment1
        blob.extend(segment2)

    total_distance = 0
    for d in distance_list:
        total_distance += d
    total_distance = total_distance + distance_increase - distance_decrease

    Result = []
    Result.append(blob)
    Result.append(total_distance)

    return Result

def find_path_index(path_list,coordinate):

    for i in range(len(path_list)):
        for c in path_list[i]:
            if(round(c[0],5)==round(coordinate[0],5) and round(c[1],5)==round(coordinate[1],5)):
                return i
    return -1

def save_to_csv(path,file_path,district_names,path_list):
    import csv
    d_name = ""
    with open(file_path,'w',newline='') as csvfile:
        fieldnames = ['origin','destination','distance','district']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i in range(len(path)):
            pos = find_path_index(path_list,path[i])
            if(pos==-1):
                d_name = "not found"
            else:
                d_name = district_names[pos]
            distance = get_distance_and_time(path[i],path[(i+1) % len(path)])[0]
            writer.writerow(
                {'origin':path[i],
                 'destination':path[(i+1) % len(path)],
                 'distance':distance,
                'district':d_name,
                })


##COUNTRY FUNCTIONS

def return_index(List,element):
    for i in range(len(List)):
        if List[i]==element:
            return i
    return -1








