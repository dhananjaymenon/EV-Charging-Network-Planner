## k = (km/kWh)
import csv
csv_file_path = "D://Dhananjay/VIT/8th Semester/0. R/Car/"
csv_file_path = "EV Car Data/"
csv_file_name = "CarCSV.csv"

class Car:
    def __init__(self,name,charge_percentage):
        self.battery_capacity = -1.0
        self.charge_power = -1.0
        self.mileagekm = -1.0
        self.k = -1.0

        self.distance_covered = 0
        with open(csv_file_path+csv_file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                if(row[0]==name):
                    self.battery_capacity = float(row[1])
                    self.charge_power = float(row[2])
                    self.mileagekm = float(row[3])
                    self.k = float(row[4])
                    break
        if self.k == -1:
            raise Exception("Car does not exist. Check name again")
        self.current_charge = float((charge_percentage/100)*self.battery_capacity)

    def ret_charge_percentage(self):
        return (self.current_charge / self.battery_capacity)*100

    def return_current_mileage(self,economic20 = True,buffer10 = True):
        charge = self.current_charge
        if(economic20):
            charge -= self.battery_capacity*0.2
        if(buffer10):
            charge -= self.battery_capacity*0.1
        return charge*self.k


    def update_charge(self, distance_covered):
        self.current_charge -= distance_covered / self.k
        self.distance_covered += distance_covered

    def check_update(self,distance_covered):
        cc = self.current_charge - distance_covered/self.k
        per = (cc/self.battery_capacity)*100
        return per


    def increase_charge_ret_time(self,percent=100):
        if(percent < float(self.current_charge*100/self.battery_capacity)):
            raise Exception("Percentage should increase")

        time_HR = ( ( (percent / 100) * self.battery_capacity) - self.current_charge) / self.charge_power
        self.current_charge = (percent/100)*self.battery_capacity

        return time_HR * 3600 #Returning time in seconds





