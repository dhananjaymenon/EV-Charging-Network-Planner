from tkinter import *
from GoogleMapsPlotter import GoogleMapsPlotter
import tkintermapview

from Interface34 import Inter3
from tkinter import messagebox
from EV_Car_Route import *

#TEMP
from EV_Car_Route import Route

#MAP VIEW IMPORTS
from tkhtmlview import HTMLLabel
#from cefpython3 import cefpython as cef
from tkintermapview import TkinterMapView
import tkinterweb

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

class Inter2:

    def __init__(self,result_i1,avoid_tolls,avoid_highways):
        self.result_i1 = result_i1
        self.PSL_names = result_i1[0]
        self.Route = result_i1[1]
        self.Distance_list = result_i1[2]
        self.Time_list = result_i1[3]
        self.travel_or_charge = result_i1[4]
        self.BP_list = result_i1[5]
        print(self.Distance_list)
        self.total_distance = find_sum(self.Distance_list)
        self.total_time = find_sum(self.Time_list)
        self.HMS_time = HMS(self.total_time)

        map_summary = GoogleMapsPlotter(self.Route,avoid_tolls,avoid_highways)
        map_summary.MapPlotter()
        to_draw_path = map_summary.extractGeoJSON()
        geo_center = map_summary.return_center()


        self.root_i2 = Tk()

        map_widget_obj = tkintermapview.TkinterMapView(self.root_i2, width=800, height=600, corner_radius=0)
        print(geo_center)
        map_widget_obj.set_position(geo_center[0],geo_center[1])
        map_widget_obj.set_zoom(6)
        #map_widget_obj.set_position(16.384944, 81.709986)
        map_widget_obj.grid(row=0,column=0)
        path_1 = map_widget_obj.set_path(to_draw_path[0])
        # print(to_draw_path[1])
        # print(self.PSL_names)
        for i in range(len(to_draw_path[1])):
            if(i==0):
                map_widget_obj.set_marker(to_draw_path[1][i][0],to_draw_path[1][i][1], text="Origin")
                continue
            if(i==len(to_draw_path[1])-1):
                map_widget_obj.set_marker(to_draw_path[1][i][0], to_draw_path[1][i][1], text="Destination")
                continue
            map_widget_obj.set_marker(to_draw_path[1][i][0],to_draw_path[1][i][1],text=self.PSL_names[i-1])


        Label_totalDistance = Label(self.root_i2, text=f"Total Distance {round(self.total_distance,2)} km")
        Label_totalTime = Label(self.root_i2, text=f"Total Time : {self.HMS_time[0]} hours, {self.HMS_time[1]} minutes, {self.HMS_time[2]} seconds")
        Button_breakDown = Button(self.root_i2, text="Break Down >>", command=self.BreakDown)


        #map_widget.grid(row=0,column=0)
        Label_totalDistance.grid(row=1, column=0)
        Label_totalTime.grid(row=2,column=0)
        Button_breakDown.grid(row=3, column=0)

        self.root_i2.mainloop()



    def BreakDown(self):
        self.root_i2.destroy()
        I3 = Inter3(self.result_i1)

        return

    def display(self):
        print(self.total_distance)


def main():
    #res = Route((13.58256,77.54236),(14.76656,77.60004),80,"Tesla S")
    res = Route((12.76333, 78.32006), (18.96319, 84.47240), 80.0, "Tesla S")

    Result_f = res.route_planner(avoid_tolls=True,avoid_highways=True)

    # print(Result[0])
    # print(Result[1])
    # print(Result[2])
    # print(Result[3])
    # #print(convert_time(Result[3]))
    # print(Result[4])
    # print(Result[5])

    R0 = ['Bharat Petroleum  Petrol Pump -N.Kuppu Rao', 'HP Petrol Pump', 'ESSAR+ petrol bunk']
    R1 = [(12.76333, 78.32006), [15.0462, 79.99985], [16.62769, 81.74077], [18.52431, 84.01685], (18.96319, 84.4724)]
    R2 = [392.833, 358.586, 386.371, 90.367]
    R3 = [26171, 959.6349000171364, 23087, 875.9743714442138, 28860, 943.8491571597116, 6907]
    R4 = [0, 1, 0, 1, 0, 1]
    R5 = [9.851249998747338, 80.0, 15.966785713142265, 80.0, 11.005178570196525, 80.0, 63.86303571399756]


    Result = []
    Result.append(R0)
    Result.append(R1)
    Result.append(R2)
    Result.append(R3)
    Result.append(R4)
    Result.append(R5)

    I2 = Inter2(Result_f,False,False)
    I2.display()

if __name__ == "__main__":
    main()
