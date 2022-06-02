import csv

def Coordinates(path,filename):
    PSL_names = []
    PSL_coordinates = []
    with open(path+filename, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            PSL_names.append(row[0])
            element = []
            element.append(float(row[1]))
            element.append(float(row[2]))
            PSL_coordinates.append(element)

    Coordinates = []
    Coordinates.append(PSL_names)
    Coordinates.append(PSL_coordinates)
    return Coordinates


