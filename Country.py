import os
from State import State
import UrlFunctions as uf
from GoogleOptimalRoute import TSP
import csv
import re

class Country:

    states = []

    def __init__(self):
        self.states = os.listdir('States/')
        print(self.states)


    def solve_all_states(self):
        solved_states = os.listdir('Result/')

        self.remaining_states = []
        for s in self.states:
            if s not in solved_states:
                self.remaining_states.append(s)

        for rs in self.remaining_states:
            S = State(rs)
            S.optimal_state()
            S.__del__()

        # state_obj_list = [State(state_name) for state_name in self.remaining_states]
        # for i in range(len(state_obj_list)):
        #     state_obj_list[i].optimal_state()
        #     del state_obj_list[i]

    def coor_from_string(self,str_c):
        str_list1 = []
        str_list2 = []
        pos = 1
        for i in range(1,len(str_c)):
            if(str_c[i]==','):
                break
            str_list1.append(str_c[i])
            pos+=1

        for i in range(pos+1,len(str_c)-1):
            str_list2.append(str_c[i])

        str1 = ''.join(str(e) for e in str_list1)
        str2 = ''.join(str(e) for e in str_list2)

        x = float(str1)
        y = float(str2)
        return [x,y]

    def optimal_route(self):
        state_coor_list = []
        # state_obj = [State(state_name) for state_name in self.states]
        # for state in state_obj:
        #     state_coor_list.append(state.ret_geocentre())
        #COORDINATES FROM CSV FILE
        csv_states = []
        csv_coordinates = []
        file_path = 'States and Districts.csv'
        file = open(file_path)
        data = csv.reader(file)

        for row in data:
            if(row[1].isalpha()):
                continue
            csv_states.append(row[0])
            x = float(row[1])
            y = float(row[2])
            csv_coordinates.append([x,y])

        #FIND AVAILABLE STATES
        for s in self.states:
            if s in csv_states:
                index = uf.return_index(csv_states,s)
                state_coor_list.append(csv_coordinates[index])
            else:
                raise Exception("State Name Error")

        matrix = uf.generate_distancematrix(state_coor_list)
        solve_tsp = TSP(matrix)
        path_and_distance = solve_tsp.return_solution()
        path = path_and_distance[0]
        path.pop()

        state_optimal_path = []
        for i in path:
            state_optimal_path.append(self.states[i])

        path_list = []
        distance_list = []
        for state in state_optimal_path:
            file_path = f'Result/{state}/0. Optimal Route.csv'
            file = open(file_path)
            data = csv.reader(file)
            path = []
            d_list = []
            for row in data:
                if(row[0].isalpha() or row[0]==''):
                    continue
                print(row[0])
                coor = self.coor_from_string(row[0])
                x = coor[0]
                y = coor[1]
                path.append([x, y])
                d_list.append(float(row[2]))
            path_list.append(path)
            distance_list.append(d_list[-1])

        print(path_list)
        print(distance_list)

        country_optimalroute_and_distance = uf.connector(path_list,distance_list)
        optimal_route = country_optimalroute_and_distance[0]
        optimalroute_distance = country_optimalroute_and_distance[1]

        self.save_to_csv(optimal_route,'Result/India Optimal Route.csv',state_optimal_path,path_list,optimalroute_distance)



    def save_to_csv(self,path,file_path,state_optimal_path,path_list,total_distance):
        s_name = ""
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['origin', 'destination', 'distance', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for i in range(len(path)):
                pos = uf.find_path_index(path_list, path[i])
                if (pos == -1):
                    s_name = "not found"
                else:
                    s_name = state_optimal_path[pos]

                distance = uf.get_distance_and_time(path[i], path[(i + 1) % len(path)])[0]


                writer.writerow(
                    {'origin': path[i],
                     'destination': path[(i + 1) % len(path)],
                     'distance': distance,
                     'state': s_name,
                     })
            writer.writerow(
                {
                    'distance': total_distance,
                })




C = Country()
C.solve_all_states()
C.optimal_route()