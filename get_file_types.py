import json

with open('files_data.json', 'r') as file:
    data = json.load(file)

file_types = {}

for filename, __ in data.items():
    file_ext = (filename.split("."))[-1]
    if file_ext not in file_types:
        file_types[file_ext] = 0
    file_types[file_ext] += 1;

print(file_types)
