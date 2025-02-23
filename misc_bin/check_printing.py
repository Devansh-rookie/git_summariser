import json


with open('files_data.json', 'r') as file:
    data = json.load(file)


for _, dat in data.items():
    print(dat)
