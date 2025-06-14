import json
import sys






def get_request_dict(new_request, path_for_request):
    with open(f"requests_page_{path_for_request}{new_request}.json", "r") as file:
        req_dict = json.load(file)

    return req_dict




def run(new_request, path_for_request, search_terms):
    filter_active = False
    request_dict = get_request_dict(new_request, path_for_request)



    #filter-system for requests, where was a hyperlink implemented

    for term in search_terms:
        if term in request_dict["description"]:
            filter_active = True

    if filter_active:
        print(f"Die Request #{new_request} entaelt Links.")
    else:
        print(f"Die Request #{new_request} enthaelt keine Links.")









if __name__ == "__main__":
    path_for_request = f"../data/Datensatz/requests/requests/"

    search_terms = ["</a>", "http", ".de", ".com", ".tt", ".ru", ".co"]
    new_request = f"#{sys.argv[1]}"  # arg: 16773-2025

    run(new_request, path_for_request, search_terms)
