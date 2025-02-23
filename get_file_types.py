import json

with open('files_data.json', 'r') as file:
    data = json.load(file)

file_types = {}
totalFiles = 0;

for filename, __ in data.items():
    file_ext = (filename.split("."))[-1]
    if file_ext not in file_types:
        file_types[file_ext] = 0
    file_types[file_ext] += 1;
    totalFiles+=1

for types, num in file_types.items():
    percentage = (num/totalFiles)*100
    file_types[types] = percentage


with open("file_types.json", 'w') as f:
    json.dump(file_types, f)

print(file_types)
