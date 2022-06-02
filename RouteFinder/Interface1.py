from tkinter import *
from tkinter import messagebox
from EV_Car_Route import *

from Interface2 import Inter2

root_i1 = Tk()
class Inter1:
    def __init__(self):

        Car_Names = [
            "MG ZS EV",
            "Tata Tigor EV",
            "Tata Nexon EV",
            "Mini Cooper SE",
            "Jaguar I-Pace",
            "BMW iX xDrive40",
            "Porsche Taycan",
            "BYD E6",
            "Audi e-tron 55 quattro",
            "Tesla S",
            "Tesla 3",
            "Tesla X",
            "Tesla Y",
        ]

        LabelX1 = Label(root_i1, text="Latitude")
        LabelY1 = Label(root_i1, text="Longitude")
        LabelX2 = Label(root_i1, text="Latitude")
        LabelY2 = Label(root_i1, text="Longitude")
        Label_origin = Label(root_i1, text="Origin")
        Entry_origin_Lat = Entry(root_i1, width=50, borderwidth=5)
        Entry_origin_Lng = Entry(root_i1, width=50, borderwidth=5)
        Label_destination = Label(root_i1, text="Destination")
        Entry_destination_Lat = Entry(root_i1, width=50, borderwidth=5)
        Entry_destination_Lng = Entry(root_i1, width=50, borderwidth=5)

        car_brand = StringVar()
        car_brand.set("Choose Vehicle")
        Choose_vehicle = OptionMenu(root_i1, car_brand, *Car_Names)
        Label_batteryPercentage = Label(root_i1, text="Current Vehicle Battery Percentage")
        Entry_batteryPercentage = Entry(root_i1, width=20, borderwidth=5)

        avoid_highways = IntVar()
        avoid_tolls = IntVar()

        Check_highways = Checkbutton(root_i1, text="Avoid Highways", variable=avoid_highways)
        Check_tolls = Checkbutton(root_i1, text="Avoid Tolls", variable=avoid_tolls)

        #Entry_Button = Button(root_i1, text="Enter", command=detailsEntered)
        Entry_Button = Button(root_i1, text="Enter",
                              command=lambda: self.detailsEntered(Entry_origin_Lat.get(),Entry_origin_Lng.get(), Entry_destination_Lat.get(), Entry_destination_Lng.get(),
                            car_brand.get(), Entry_batteryPercentage.get(),avoid_highways,avoid_tolls))

        ##DEFAULT TEXT##
        Entry_origin_Lat.insert(END, '12.76333')
        Entry_origin_Lng.insert(END, '78.32006')
        Entry_destination_Lat.insert(END, '18.96319')
        Entry_destination_Lng.insert(END, '84.4724')

        # LAYOUT
        LabelX1.grid(row=0, column=1)
        LabelY1.grid(row=0, column=2)

        Label_origin.grid(row=1, column=0)
        Entry_origin_Lat.grid(row=1, column=1)
        Entry_origin_Lng.grid(row=1, column=2)

        LabelX2.grid(row=2, column=1)
        LabelY2.grid(row=2, column=2)

        Label_destination.grid(row=3, column=0)
        Entry_destination_Lat.grid(row=3, column=1)
        Entry_destination_Lng.grid(row=3, column=2)

        Choose_vehicle.grid(row=4, column=0)
        Label_batteryPercentage.grid(row=5, column=0)
        Entry_batteryPercentage.grid(row=5, column=1)

        Check_highways.grid(row=6, column=0)
        Check_tolls.grid(row=7, column=0)

        Entry_Button.grid(row=8, column=1)

        root_i1.mainloop()
        # self.detailsEntered(Entry_origin_Lat.get(),Entry_origin_Lng.get(), Entry_destination_Lat.get(), Entry_destination_Lng.get(),
        #                     car_brand.get(), Entry_batteryPercentage.get(),avoid_highways,avoid_tolls)

    def detailsEntered(self,Entry_origin_Lat,Entry_origin_Lng, Entry_destination_Lat, Entry_destination_Lng,
                          car_brand, Entry_batteryPercentage,avoid_highways,avoid_tolls):
        #print(car_brand.get())
        self.checkEntries(Entry_origin_Lat, Entry_origin_Lng, Entry_destination_Lat, Entry_destination_Lng,
                          car_brand, Entry_batteryPercentage)

        ##TERMINATE INTER 1 HERE
        root_i1.destroy()

        o_lat = float(Entry_origin_Lat)
        o_lng = float(Entry_origin_Lng)
        d_lat = float(Entry_destination_Lat)
        d_lng = float(Entry_destination_Lng)
        b_Percentage = float(Entry_batteryPercentage)

        R1 = Route((o_lat,o_lng),(d_lat,d_lng),b_Percentage,car_brand)
        a_highways = False
        a_tolls = False
        if(avoid_highways==1):
            a_highways = True

        if(avoid_tolls==1):
            a_tolls = True

        Result = R1.route_planner(avoid_tolls=a_tolls,avoid_highways=a_highways)
        print(Result[0])
        print(Result[1])
        print(Result[2])
        print(Result[3])
        print(convert_time(Result[3]))
        print(Result[4])
        print(Result[5])


        I2 = Inter2(Result,a_tolls,a_highways)
        I2.display()



    def checkEntries(self,Entry_origin_Lat,Entry_origin_Lng,Entry_destination_Lat,Entry_destination_Lng,car_brand, Entry_batteryPercentage):
        if Entry_origin_Lat=='' \
            or Entry_origin_Lng=='' \
            or Entry_destination_Lat=='' \
            or Entry_destination_Lng=='' :
            messagebox.showerror("Missing Parameter", "Please Enter all coordinates")
            return


        if (float(Entry_origin_Lat)>90 or float(Entry_origin_Lat)<-90) \
            or (float(Entry_destination_Lat)>90 or float(Entry_destination_Lat)<-90) \
            or (float(Entry_origin_Lng) > 180 or float(Entry_origin_Lng) < -180) \
            or (float(Entry_destination_Lng)>180 or float(Entry_destination_Lng)<-180):
            messagebox.showerror("Incorrect Parameter", "Wrong Coordinates Entered")
            return

        if (car_brand == "Choose Vehicle"):
            messagebox.showerror("Missing Parameter", "Please choose a vehicle")
            return

        if(Entry_batteryPercentage==''):
            messagebox.showerror("Missing Parameter", "Please enter current vehicle percentage")
            return


def main():
    interface_1 = Inter1()

if __name__ == "__main__":
    main()