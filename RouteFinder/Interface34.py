from tkinter import *
import tkintermapview
import AdditionalFunctions as af
#from Interface4 import Inter4
import requests
import json
from tkinter import messagebox

class Inter3:

    def __init__(self,result_i1):
        self.result_i1 = result_i1
        self.PSL_names = result_i1[0]
        self.Route = result_i1[1]
        self.Distance_list = result_i1[2]
        self.Time_list = result_i1[3]
        self.travel_or_charge = result_i1[4]
        self.BP_list = result_i1[5]
        #print(self.Distance_list)
        self.total_distance = af.find_sum(self.Distance_list)
        self.total_time = af.find_sum(self.Time_list)
        self.HMS_time = af.HMS(self.total_time)

        #FOR FRAME NUMBERS
        self.frame_number = 0
        self.number_of_frames = len(self.travel_or_charge)


        self.root_i3 = Tk()
        self.frame()
        self.root_i3.mainloop()


    def next(self):
        #self.frame_number = (self.frame_number + 1) % self.number_of_frames
        self.frame_number = self.frame_number + 1
        self.frame()

    def previous(self):
        #self.frame_number = (self.frame_number - 1) % self.number_of_frames
        self.frame_number = self.frame_number - 1
        self.frame()

    def nearbyattractions(self):
        pin = int((self.frame_number + 1) / 2)
        ps_name = self.PSL_names[pin - 1]
        location = self.Route[pin]
        time_in_seconds = self.Time_list[self.frame_number]
        place_types = ["bakery","bar","cafe","meal_takeaway","restaurant"]

        url_string = af.nearby_places_url(location, time_in_seconds, place_types)

        json_data = requests.get(url_string).json()
        with open('NA/attractionsnearby.json', 'w') as json_file:
            json.dump(json_data, json_file)

        place_list = af.JSON_to_placeList('NA/attractionsnearby.json')

        if (len(place_list) == 0):
            messagebox.showinfo("Nearby Attractions", "There are no nearby attractions")

        else:
            self.root_i3.destroy()
            I4 = Inter4(self.PSL_names[pin - 1], self.Route[pin], self.Time_list[self.frame_number], self.result_i1)


    def frame(self):


        for widgets in self.root_i3.winfo_children():
            widgets.destroy()
        to_draw_path = af.extractGeoJSON(self.Route)
        map_widget_obj = tkintermapview.TkinterMapView(self.root_i3, width=800, height=600, corner_radius=0)
        map_widget_obj.grid(row=0,column=0,columnspan=2)
        print(f'{self.frame_number} JAJAJA pos')
        print(self.BP_list)
        print(self.number_of_frames)
        print(self.travel_or_charge)

##CH CH CH CH CHANGES
        if(self.travel_or_charge[self.frame_number]==0 ):
            pos = int(self.frame_number / 2)
            geo_x = float(self.Route[pos][0] + self.Route[pos + 1][0]) / 2
            geo_y = float(self.Route[pos][1] + self.Route[pos + 1][1]) / 2
            geo_center = [geo_x, geo_y]
            print(geo_center)
            map_widget_obj.set_position(geo_center[0], geo_center[1])
            map_widget_obj.set_zoom(7)

        else:
            pos = int((self.frame_number + 1) / 2)
            geo_x = self.Route[pos][0]
            geo_y = self.Route[pos][1]
            geo_center = [geo_x, geo_y]
            print(geo_center)
            map_widget_obj.set_position(geo_center[0], geo_center[1])
            map_widget_obj.set_zoom(9)

        Label_Distance = Label(self.root_i3, text=f"Distance {round(self.Distance_list[pos], 2)} km")
        Label_Distance.grid(row=1, column=0)

        Button_nearbyattractions = Button(self.root_i3, text="nearby attractions", bg='blue', fg='white',
                                          command=self.nearbyattractions)
        Button_nearbyattractions.grid(row=1, column=0)


        HMS_format = af.HMS(self.Time_list[self.frame_number])
        Label_TimeTaken = Label(self.root_i3, text=f"Time Taken {HMS_format[0]} hours, {HMS_format[1]} minutes")
        Label_TimeTaken.grid(row=2, column=0)
        Label_BatteryPercentage = Label(self.root_i3,
                                        text=f"Final Battery Percentage {round(self.BP_list[self.frame_number], 0)} %")
        Label_BatteryPercentage.grid(row=2, column=1)

        if (self.travel_or_charge[self.frame_number] == 0):
            Button_nearbyattractions.grid_forget()
        else:
            Label_Distance.grid_forget()

        #PATH SPLITTER
        if(self.travel_or_charge[self.frame_number]==0 ):
            paths = af.path_splitter(to_draw_path[0],self.Route[pos],self.Route[pos+1])
            path_1 = map_widget_obj.set_path(paths[0])
            path_2 = map_widget_obj.set_path(paths[1],color="orange")
            path_3 = map_widget_obj.set_path(paths[2])
        else:
            path_1 = map_widget_obj.set_path(to_draw_path[0])
        Button_next = Button(self.root_i3, text=">>", command=self.next)
        Button_previous = Button(self.root_i3, text="<<",command=self.previous)
        Button_previous.grid(row=3, column=0)
        Button_next.grid(row=3, column=1)

        if(self.frame_number==0):
            Button_previous.destroy()
        if(self.frame_number==self.number_of_frames-1):
            Button_next.grid_forget()


        pin = -1
        if (self.travel_or_charge[self.frame_number] == 1):
            pin = (self.frame_number+1) / 2

        for i in range(len(to_draw_path[1])):
            if(i==pin):
                map_widget_obj.set_marker(to_draw_path[1][i][0], to_draw_path[1][i][1], text=self.PSL_names[i - 1])
                continue
            if (i == 0):
                map_widget_obj.set_marker(to_draw_path[1][i][0], to_draw_path[1][i][1], text="Origin",marker_color_circle="black",marker_color_outside="grey")
                continue
            if (i == len(to_draw_path[1]) - 1):
                map_widget_obj.set_marker(to_draw_path[1][i][0], to_draw_path[1][i][1], text="Destination",marker_color_circle="black",marker_color_outside="grey")
                continue
            map_widget_obj.set_marker(to_draw_path[1][i][0], to_draw_path[1][i][1], text=self.PSL_names[i - 1],marker_color_circle="black",marker_color_outside="grey")

class Inter4:

    def __init__(self,ps_name,coordinate,time,history_result):
        self.result_i3 = history_result
        self.ps_name = ps_name
        self.location = coordinate
        self.time_in_seconds = time
        self.place_types = ["bakery","bar","cafe","meal_takeaway","restaurant"]
        #self.empty = 0

        url_string = af.nearby_places_url(self.location,self.time_in_seconds,self.place_types)

        json_data = requests.get(url_string).json()
        with open('NA/attractionsnearby.json','w') as json_file:
            json.dump(json_data, json_file)

        self.place_list = af.JSON_to_placeList('NA/attractionsnearby.json')
        # if(len(self.place_list) == 0):
        #     messagebox.showinfo("Nearby Attractions", "There are no nearby attractions")
        #     I3 = Inter3(self.result_i3)
        #     #self.empty = 1
        # else:

        self.display_list()


    def back_to_I3(self):
        self.root_i4.destroy()
        I3 = Inter3(self.result_i3)
        return

    def back_to_NA(self):
        self.root_fr.destroy()
        #self.root_i4 = Tk()
        self.display_list()
        #self.root_i4.mainloop()

    def find_route(self,na):
        origin_name = self.ps_name
        origin_location = self.location
        destination_name = self.place_list[na].name
        destination_location = self.place_list[na].location
        self.root_i4.destroy()


        self.root_fr = Tk()
        Button_backToI4 = Button(self.root_fr, text="< Back to Nearby Attractions", command=self.back_to_NA)
        Button_backToI4.grid(row=0, column=0)

        map_widget_obj = tkintermapview.TkinterMapView(self.root_fr, width=800, height=600, corner_radius=0)
        map_widget_obj.set_position(origin_location[0], origin_location[1])
        map_widget_obj.set_zoom(15)
        map_widget_obj.grid(row=1, column=0)
        path_to_draw = af.walking_route(origin_location,destination_location,"NA/directions.json")
        path_1 = map_widget_obj.set_path(path_to_draw)

        map_widget_obj.set_marker(origin_location[0],origin_location[1],text=origin_name)
        map_widget_obj.set_marker(destination_location[0],destination_location[1],text=destination_name)

        self.root_fr.mainloop()

        return

    def display_list(self):
        self.root_i4 = Tk()
        for widgets in self.root_i4.winfo_children():
            widgets.destroy()

        Button_backToI3 = Button(self.root_i4,text="< Back to Break Down", command=self.back_to_I3)
        Button_backToI3.grid(row=0,column=0)

        map_widget_obj = tkintermapview.TkinterMapView(self.root_i4, width=800, height=600, corner_radius=0)
        map_widget_obj.grid(row=1, column=0, columnspan=2,rowspan=15)
        map_widget_obj.set_position(self.location[0],self.location[1])
        map_widget_obj.set_zoom(15)
        map_widget_obj.set_marker(self.location[0], self.location[1], text=self.ps_name)

        for pl in self.place_list:
            map_widget_obj.set_marker(pl.location[0],pl.location[1],text=pl.name,marker_color_circle="black",marker_color_outside="grey")

        Label_choose = Label(self.root_i4,text="Choose a destination")

        na = IntVar()
        na.set(0)
        pos = 1
        for i in range(len(self.place_list)):
            Radiobutton(self.root_i4, text=self.place_list[i].name, value=i, variable=na,anchor="w",width=30).grid(row=pos,column=2)
            if(self.place_list[i].rating==-1):
                Label(self.root_i4, text='No rating', font=('bold')).grid(row=pos,column=3)
                #Label(self.root_i4, text=f'{self.place_list[i].num_of_ratings} reviews').grid(row=pos, column=4)
            else:
                Label(self.root_i4,text=f'{round(self.place_list[i].rating,2)}',font=('bold')).grid(row=pos,column=3)
                Label(self.root_i4, text=f'{self.place_list[i].num_of_ratings} reviews').grid(row=pos, column=4)
            pos += 1

        Button_findRoute = Button(self.root_i4, text="Find Route", bg='blue',fg='white',command=lambda: self.find_route(na.get()))
        Button_findRoute.grid(row=pos,column=2)
        self.root_i4.mainloop()


def main():
    #res = Route((13.58256,77.54236),(14.76656,77.60004),80,"Tesla S")
    #res = Route((12.76333, 78.32006), (18.96319, 84.47240), 80.0, "Tesla S")

    #Result_f = res.route_planner(avoid_tolls=True,avoid_highways=True)

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
    R4 = [0, 1, 0, 1, 0, 1, 0 ]
    R5 = [9.851249998747338, 80.0, 15.966785713142265, 80.0, 11.005178570196525, 80.0, 63.86303571399756]


    Result = []
    Result.append(R0)
    Result.append(R1)
    Result.append(R2)
    Result.append(R3)
    Result.append(R4)
    Result.append(R5)

    I3 = Inter3(Result)


if __name__ == "__main__":
    main()
