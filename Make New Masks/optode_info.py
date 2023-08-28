import pandas as pd

def read_excel_file(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        
        # Convert DataFrame to a list of dictionaries
        nested_list = df.values.tolist()
        return nested_list
    
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def remove_first_item(nested_list):
    for sublist in nested_list:
        print(sublist[0])
        del sublist[0]

path = "C:\\Users\\Lenovo\\Desktop\\fNIRS_GLM_MPCA\\BrainRobot_8x8_Inter-optode distances.xlsx"
distances_SD = read_excel_file(path)
remove_first_item(distances_SD)

first_order_channels= [ [1, 2],
                       [1, 3],
                       [1, 4],
                       [1, 5],
                       [2, 1],
                       [2, 2],
                       [2, 3],
                       [3, 2],
                       [3, 3],
                       [3, 5],
                       [4, 1],
                       [4, 3],
                       [4, 4],
                       [4, 5],
                       [4, 6],
                       [5, 3],
                       [5, 5],
                       [5, 7],
                       [6, 4],
                       [6, 6],
                       [7, 5],
                       [7, 6],
                       [7, 7],
                       [7, 8],
                       [8, 6],
                       [8, 8]]

first_order = []
x = []
y = []
new_matrix = [[0]*8 for _ in range(8)]
for s in range(len(first_order_channels)):
    x.append(first_order_channels[s][0])
    y.append(first_order_channels[s][1])
for coor in range (len(x)):
    new_x = x[coor] - 1 
    new_y = y[coor] - 1 
    print(new_x,new_y)
    new_matrix[new_x][new_y] = 1
           # print(len(x),new_matrix)

first_order.extend(new_matrix)

print(first_order)











