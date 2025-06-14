import json
import os
import sys


id_1 = f"#{sys.argv[1]}"
id_2 = f"#{sys.argv[2]}"

getit = 0

id_1_dict: dict
id_2_dict: dict

path_for_request = f"Datensatz/requests/requests/requests_page_"


#get amount of files in every list
num_files_request = len(os.listdir("Datensatz/requests/requests"))


#filter-system for requests, where was a hyperlink implemented
for i in range(1, num_files_request):
    with open(f"{path_for_request}{i}.json", "r") as file:
        data = json.load(file)

        for request in data["rows"]:
            if id_1 in request["title"]:
                id_1_dict = request
                getit += 1
                
            if id_2 in request["title"]:
                getit += 1
                id_2_dict = request

for key in id_1_dict:
    print(f"{key}\t\t{id_1_dict[key]}\t\t{id_2_dict[key]}")



