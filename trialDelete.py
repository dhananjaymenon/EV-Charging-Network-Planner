# import os, shutil
# json_holder_name = "JsonHolder"
# folder = json_holder_name
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))
"""
Coor = '[15.38601, 79.03312]'
x = Coor[1:9]
y = Coor[-9:-1]
print(x,y)
"""

def bayesian_average(product_ratings_average,product_ratings_count):
    m = 3
    C = 25
    b_a = (product_ratings_average*product_ratings_count + m*C) / (product_ratings_count + C)
    return b_a

print(bayesian_average(4.8,100))
print(bayesian_average(4.6,1000))
print(bayesian_average(5.0,10))


def coor_from_string(str_c):
    str_list1 = []
    str_list2 = []
    pos = 1
    for i in range(1, len(str_c)):
        if (str_c[i] == ','):
            break
        str_list1.append(str_c[i])
        pos += 1

    for i in range(pos + 1, len(str_c) - 1):
        str_list2.append(str_c[i])

    str1 = ''.join(str(e) for e in str_list1)
    str2 = ''.join(str(e) for e in str_list2)

    x = float(str1)
    y = float(str2)
    return [x, y]

print(coor_from_string('[23.3456,23.76859]')[0])
print(coor_from_string('[23.3456,23.76859]')[1])

"""
import numpy as np

matrix1=[[1]]
matrix2=[[2]]
matrix3=[[3]]
matrix4=[[4]]
matrix5=[[5]]
matrix6=[[6]]
matrix7=[[7]]
matrix8=[[8]]
matrix9=[[9]]
matrix10=[[10]]
matrix11=[[11]]
matrix12=[[12]]
matrix13=[[13]]
matrix14=[[14]]
matrix15=[[15]]
matrix16=[[16]]
matrix_list = []
matrix_list.append(matrix1)
matrix_list.append(matrix2)
matrix_list.append(matrix3)
matrix_list.append(matrix4)
matrix_list.append(matrix5)
matrix_list.append(matrix6)
matrix_list.append(matrix7)
matrix_list.append(matrix8)
matrix_list.append(matrix9)
matrix_list.append(matrix10)
matrix_list.append(matrix11)
matrix_list.append(matrix12)
matrix_list.append(matrix13)
matrix_list.append(matrix14)
matrix_list.append(matrix15)
matrix_list.append(matrix16)
# matrix_list.append(matrix7)
# matrix_list.append(matrix8)
# matrix_list.append(matrix9)
# matrix7=[]
# matrix8=[]
# matrix9=[]

col_c2 = [0, 10, 10, 0, 20, 20, 20, 10, 0, 30, 30, 30, 30, 20, 10, 0, 40, 40, 40, 40, 40, 30, 20, 10, 0]
row_c2 = [0, 0, 10, 10, 0, 10, 20, 20, 20, 0, 10, 20, 30, 30, 30, 30, 0, 10, 20, 30, 40, 40, 40, 40, 40]

col_c = []
row_c = []

for i in range(len(col_c2)):
    col_c.append(int(col_c2[i]/10))
    row_c.append(int(row_c2[i]/10))

print(col_c)
print(row_c)

num = 4

megamatrix = np.zeros((num, num), dtype=int)

for i in range(len(matrix_list)):

    for row in range(len(matrix_list[i])):

        for col in range(len(matrix_list[i][0])):
            megamatrix[row + row_c[i]][col + col_c[i]] = matrix_list[i][row][col]


for row in megamatrix:
    for col in row:
        print(col,end="\t")
    print()
"""