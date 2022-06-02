import math
import APIKey
import UrlFunctions as uf
import os
from District import District
from GoogleOptimalRoute import TSP




class State:
    districts = []

    def __del__(self):
        print()

    def __init__(self,name):
        self.name = name
        self.dir_list = os.listdir(f'States/{name}/')
        for i in self.dir_list:
            self.districts.append(i[:-4])
        #self.districts = [f.path for f in os.scandir(f'States/{name}/') if f.is_dir()]
        print(self.districts)

    def ret_geocentre(self):
        geoX = 0.0
        geoY = 0.0
        district_obj_list = [District(self.name, district_name) for district_name in self.districts]
        for i in range(len(district_obj_list)):
            district_coor = district_obj_list[i].ret_geocentre()
            geoX += district_coor[0]
            geoY += district_coor[1]
            del district_obj_list[i]
        geoX = geoX/len(district_obj_list)
        geoY = geoY/len(district_obj_list)
        return [geoX,geoY]


    def optimal_district(self,district_name):
        D = District(self.name,district_name)
        path_and_distance = D.TSP_Solver()
        print(path_and_distance[0])
        print(path_and_distance[1])

    def optimal_state(self):
        district_coor = []
        district_obj = [District(self.name,district_name) for district_name in self.districts]
        for i in range(len(district_obj)):
            #obj.set_values()
            district_coor.append(district_obj[i].ret_geocentre())
            print(district_obj[i].ret_geocentre())
            #del district_obj[i]

        matrix = uf.generate_distancematrix(district_coor)
        print("LOOKOKOK")
        print(district_coor)
        solve_tsp = TSP(matrix)
        path_and_distance = solve_tsp.return_solution()
        path = path_and_distance[0]
        path.pop()

        district_optimal_path = []
        for i in path:
            district_optimal_path.append(self.districts[i])

        path_list = []
        distance_list = []
        district_obj2 = [District(self.name,district_name) for district_name in district_optimal_path]

        ##CHECK STATE DIRECTORY##
        if(not os.path.isdir(f'Result/{self.name}')):
            os.mkdir(f'Result/{self.name}')

        counter = 1
        for obj in district_obj2:
            p_and_d = obj.TSP_Solver()
            p = p_and_d[0]
            d = p_and_d[1]
            path_list.append(p)
            distance_list.append(d)
            obj.write_to_csv(f'Result/{self.name}/{counter}. {obj.district_name}.csv') # 1. Anantapur.csv
            counter+=1
            del obj

        optimalroute_and_distance = uf.connector(path_list,distance_list)
        optimal_route = optimalroute_and_distance[0]
        optimalroute_distance = optimalroute_and_distance[1]

        self.save_to_csv(optimal_route,f'Result/{self.name}/0. Optimal Route.csv',district_optimal_path,path_list,optimalroute_distance)
        print("OPTIMAL DISTRICT PATH")
        print(district_optimal_path)
        print("-------------------")
        print("DISTANCE LIST")
        print(distance_list)
        print("---------------")
        print(optimal_route)
        print(optimalroute_distance)

    def save_to_csv(self,path, file_path, district_names, path_list,total_distance):
        import csv
        d_name = ""
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['origin', 'destination', 'distance', 'district']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for i in range(len(path)):
                pos = uf.find_path_index(path_list, path[i])
                if (pos == -1):
                    d_name = "not found"
                else:
                    d_name = district_names[pos]
                distance = uf.get_distance_and_time(path[i], path[(i + 1) % len(path)])[0]
                writer.writerow(
                    {'origin': path[i],
                     'destination': path[(i + 1) % len(path)],
                     'distance': distance,
                     'district': d_name,
                     })
            writer.writerow(
                {
                 'distance': total_distance,
                })
def main():
    #S = State('Andhra Pradesh')
    S = State('Kerala')
    S.optimal_state()
    # #S.optimal_district('Anantapur')
    # S.optimal_state()

if __name__ == "__main__":
    main()
