import json
import os





path_for_request = f"../data/Datensatz/requests/requests/requests_page_"

search_terms = ["</a>", "http", ".com", ".de"]



filtered_request_id = []


#get amount of files in every list
num_files_request = len(os.listdir("../data/Datensatz/requests/requests"))



#filter-system for requests, where was a hyperlink implemented
for i in range(1, num_files_request):
    with open(f"{path_for_request}{i}.json", "r") as file:
        data = json.load(file)

        for request in data["rows"]:
            for term in search_terms:
                if term in request["description"]:
                    if not request["service_request_id"] in filtered_request_id:
                    
                        with open(f"../data/filtered_data/{request["title"][1:]}.json", "w") as new_file:
                            json.dump(request, new_file, indent=4, ensure_ascii=False)
                        
                        filtered_request_id.append(request["service_request_id"])
            
print(filtered_request_id)
print(len(filtered_request_id))



