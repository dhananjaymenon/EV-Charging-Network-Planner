from Car import Car
import PetrolStationList as psl
from geopy import distance
import requests
from urllib.parse import urlencode, urlparse, parse_qsl
import AdditionalFunctions as af
import APIKey
api_key = APIKey.api_key

def index_list(n):
    List = []
    for i in range(n):
        List.append(i)
    return List

#PSL = psl.Coordinates("D://Dhananjay/VIT/8th Semester/0. R/Petrol Planning/","PSLtrial.csv")
PSL = psl.Coordinates("EV Station Data/","PSLtrial.csv")
PetrolStation_names = PSL[0]
PetrolStation_indexes = index_list(len(PSL[0]))
List_of_PetrolStations = PSL[1]

def quick_sort(s,c):
    if len(s) == 1 or len(s) == 0:
        return c
    else:
        pivot = s[0]
        i = 0
        for j in range(len(s) - 1):
            if s[j + 1] < pivot:
                s[j + 1], s[i + 1] = s[i + 1], s[j + 1]
                c[j + 1], c[i + 1] = c[i + 1], c[j + 1]
                i += 1
        s[0], s[i] = s[i], s[0]
        c[0], c[i] = c[i], c[0]
        first_part = quick_sort(s[:i],c[:i])
        second_part = quick_sort(s[i + 1:],c[i + 1:])
        first_part.append(c[i])
        return first_part + second_part

def convert_time(List):
    converted_time = []
    for L in List:
        hrs = int(L/3600)
        min = int((L%3600)/60)
        sec = L%60
        HMS = []
        HMS.append(hrs)
        HMS.append(min)
        HMS.append(sec)
        converted_time.append(HMS)
    return converted_time



class Route:

    def __init__(self, origin, destination, charge_percentage, car_brand):
        #ORIGIN AND DESTINATION
        self.origin = origin
        self.destination = destination

        #CAR
        self.EV_car = Car(car_brand,charge_percentage)

        self.route = []
        self.index_route = []

    def ret_pslnamesList(self):
        Result = []
        print(self.index_route)
        for i in self.index_route:
            Result.append(PetrolStation_names[i])
        return Result

    def get_distance_and_time(self,origin,destination,avoid_tolls, avoid_highways):
        avoid_string = "ferries,indoor"
        if(avoid_tolls):
            avoid_string = avoid_string + ",tolls"
        if(avoid_highways):
            avoid_string = avoid_string + ",highways"
        origin_url = str(origin[0]) + "," + str(origin[1]) + "|"
        destination_url = str(destination[0]) + "," + str(destination[1]) + "|"
        data_type = "json"
        endpoint = f"https://maps.googleapis.com/maps/api/distancematrix/{data_type}"
        params = \
            {"origins": origin_url,
             "destinations": destination_url,
             "mode":"driving",
             "avoid":avoid_string,
             "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        print(url)
        r = requests.get(url)
        #print(r.json())
        #print(r.json()['rows'][0]['elements'][0]['distance']['text'])
        distance = r.json()['rows'][0]['elements'][0]['distance']['value']
        distance_km = float(distance/1000)
        time = r.json()['rows'][0]['elements'][0]['duration']['value']
        R = []
        R.append(distance_km)
        R.append(time)
        return R

    def find_chargestation(self,origin,destination, mileageKM,avoid_tolls,avoid_highways):
        alpha = 0.5
        candidates = []
        d1d2_list = []
        d3_list = []
        score = []

        for i in List_of_PetrolStations:
            #print(i,origin)
            if i in self.route:
                continue
            if(distance.distance(i,origin).km<mileageKM and distance.distance(i,destination).km <  distance.distance(origin,destination).km):
                candidates.append(i)
                d1 = distance.distance(i, origin).km
                d2 = distance.distance(i, destination).km
                d3 = mileageKM - distance.distance(i,origin).km
                d1d2_list.append(d1 + d2)
                d3_list.append(d3)




        if(len(candidates)==0):
            for i in List_of_PetrolStations:
                if i in self.route:
                    continue
                if (distance.distance(i, origin).km < mileageKM):
                    candidates.append(i)
                    d1 = distance.distance(i, origin).km
                    d2 = distance.distance(i, destination).km
                    d3 = mileageKM - distance.distance(i, origin).km
                    d1d2_list.append(d1 + d2)
                    d3_list.append(d3)

        if (len(candidates) == 0):
            raise Exception('Cannot reach charge station')

        candidatesd1d2 = quick_sort(d1d2_list,candidates)
        candidatesd3 = quick_sort(d3_list,candidates)

        print(candidates)
        print(candidatesd1d2)
        print(candidatesd3)
        min_score = float('inf')
        ideal_candidate = []


        for j in range(len(candidates)):
            score.append(float ( (alpha)*candidatesd1d2.index(candidates[j]) + (1-alpha)*candidatesd3.index(candidates[j]) ) )

            dist = self.get_distance_and_time(origin,candidates[j],avoid_tolls,avoid_highways)[0]
            per = self.EV_car.check_update(dist)
            if(score[j] < min_score and per>15.0):
                ideal_candidate = candidates[j]
                min_score = score[j]

        if(len(ideal_candidate)==0):
            raise Exception("Cannot reach destination")

        ideal_candidate_index = List_of_PetrolStations.index(ideal_candidate)
        self.index_route.append(ideal_candidate_index)
        return ideal_candidate

    def return_function(self,PSLN,R,D,T,TI,BP):
        List = []
        List.append(PSLN)
        List.append(R)
        List.append(D)
        List.append(T)
        List.append(TI)
        List.append(BP)
        return List


    def route_planner(self, avoid_tolls=False, avoid_highways=False):
        print(self.EV_car.ret_charge_percentage())
        origin = self.origin
        destination = self.destination
        reached_destination = False
        #route = []
        time = 0
        distance = 0

        time_list = []
        distance_list = []
        time_index = [] # 0 in travel, 1 is charging
        charge_percentage = []

        self.route.append(origin)
        while(not reached_destination):
            if(self.EV_car.current_charge<0):
                raise Exception("Charge Cannot be Negative")
            o2d = self.get_distance_and_time(origin,destination,avoid_tolls,avoid_highways)
            o2d_distance = o2d[0]

            #print(o2d_distance, self.EV_car.mileage(self.charge))
            print(type(o2d_distance))

            if self.EV_car.return_current_mileage(buffer10=False) > o2d_distance:
                self.route.append(destination)
                distance += o2d_distance
                distance_list.append(o2d_distance)
                o2d_time = o2d[1]
                time_list.append(o2d_time)

                time += o2d_time

                #Update Charge
                self.EV_car.update_charge(o2d_distance)
                charge_percentage.append(self.EV_car.ret_charge_percentage())
                print(self.EV_car.ret_charge_percentage())
                reached_destination = True

                time_index.append(0)


            else:
                nearest_charging_station = self.find_chargestation(origin,destination,self.EV_car.return_current_mileage(buffer10=False),avoid_tolls,avoid_highways)
                self.route.append(nearest_charging_station)

                #TRAVELLING TO CHARGING STATION
                distance_and_time = self.get_distance_and_time(origin,nearest_charging_station,avoid_tolls,avoid_highways)
                distance += distance_and_time[0]
                distance_list.append(distance_and_time[0])
                time += distance_and_time[1]
                time_list.append(distance_and_time[1])
                time_index.append(0)
                self.EV_car.update_charge(distance_and_time[0])
                charge_percentage.append(self.EV_car.ret_charge_percentage())
                print(self.EV_car.ret_charge_percentage())

                #CHARGING AT CHARGING STATION
                time_charge = self.EV_car.increase_charge_ret_time(percent=80)
                time += time_charge
                time_list.append(time_charge)
                time_index.append(1)
                charge_percentage.append(self.EV_car.ret_charge_percentage())
                print(self.EV_car.ret_charge_percentage())

                #Change origin
                origin = nearest_charging_station

        return self.return_function(self.ret_pslnamesList(),self.route,distance_list,time_list,time_index,charge_percentage)

def main():
    #R1 = Route((13.58256,77.54236),(14.76656,77.60004),80,"Tesla S")
    R1 = Route((12.76333, 78.32006), (18.96319, 84.47240), 80, "Tesla S")

    Result = R1.route_planner(avoid_tolls=False,avoid_highways=False)

    print(Result[0])
    print(Result[1])
    print(Result[2])
    print(convert_time(Result[3]))
    print(Result[4])
    print(Result[5])

if __name__ == "__main__":
    main()