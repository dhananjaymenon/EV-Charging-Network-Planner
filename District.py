import math
import APIKey
import UrlFunctions as uf
import csv


class District:

    def __del__(self):
        print()

    def __init__(self,state_name,district_name):
        self.route_coor = []
        self.route_names = []
        self.geocentre = []
        self.state_name = state_name
        self.district_name = district_name
        self.geoX = 0.0
        self.geoY = 0.0

    #def set_values(self):
        #CSV READER
        file_path = f'States/{self.state_name}/{self.district_name}.csv'
        file = open(file_path,encoding="utf8")
        data = csv.reader(file)

        for row in data:
            self.route_names.append(row[0])
            X = []
            X.append(float(row[1]))
            self.geoX += float(row[1])
            X.append(float(row[2]))
            self.route_coor.append(X)
            self.geoY += float(row[2])
        print(self.route_coor)

        self.geoX = self.geoX / len(self.route_coor)
        self.geoY = self.geoY / len(self.route_coor)

    def ret_geocentre(self):
        print("FFFF")
        return [self.geoX,self.geoY]



    def TSP_Solver(self):
        CXkm = []
        CYkm = []
        for i in self.route_coor:
            CXkm.append(i[0])
            CYkm.append(i[1])

        url_list = uf.url_generator(CXkm,CYkm)
        uf.save_json_files(url_list)
        path_and_distance = uf.json_to_path(len(CXkm),self.route_coor)
        return path_and_distance

    def write_to_csv(self,file_path):
        import csv

        with open(file_path,'w',newline='',encoding="utf8") as csvfile:
            fieldnames = ['origin', 'destination', 'distance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            p_and_d = self.TSP_Solver()
            path = p_and_d[0]
            d = p_and_d[1]
            for i in range(len(path)):

                distance = uf.get_distance_and_time(path[i], path[(i + 1) % len(path)])[0]
                writer.writerow(
                    {'origin': path[i],
                     'destination': path[(i + 1) % len(path)],
                     'distance': distance,
                     })
            writer.writerow(
                {'distance': d}
            )

        print(f"TOTAL DISTANCE : {p_and_d[1]}")


# D = District('Andhra Pradesh','Chitoor')
# D.write_to_csv('Result/trialCh.csv')



