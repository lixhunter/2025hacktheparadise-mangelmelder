import json
import os
import sys
import datetime
import re
from typing import List, Dict
from math import radians, sin, cos, atan2, sqrt

new_request = f"#{sys.argv[1]}"

def get_request_dict(request_id):
    req_dict: dict

    print(request_id[1:])
    with open(f"../data/cloud-jena/maengel/{request_id[1:]}.json", "r") as file:
    ##with open(f"data/duplicates/{request_id[1:]}.json", "r") as file:
        req_dict = json.load(file)

    return req_dict



def dublicate_prefilter(newReport:  Dict) -> List[Dict]:
    directory = "../data/cloud-jena/maengel"

    files = [f for f in os.listdir(directory) if f.endswith('.json')]

    reports = []
    for fname in files:
        with open(os.path.join(directory, fname), "r", encoding='utf-8') as f:
            report = json.load(f)
            reports.append(report)

    recent_reports = filter_by_timeSpan(reports)

    near_reports = filter_by_radius(newReport, recent_reports, radius_meters=300)

    return near_reports

#TODO: if duplicate_prefilter returns something, send to llm for final duplicate check

def extract_datetime(text) -> datetime.datetime:
    match = re.search(r'datetime=\"([^\"]+)\"', text)
    if match:
        return datetime.datetime.fromisoformat(match.group(1))
    return None


def filter_by_timeSpan(entries: List[Dict]) -> List[Dict]:

    now = datetime.datetime.now(datetime.timezone.utc)
    two_months_ago = now - datetime.timedelta(days=60)

    return [item for item in entries
            if extract_datetime(item['requested_datetime']) is not None
            and extract_datetime(item['requested_datetime']) >= two_months_ago]   


def calculate_distance_km(lat1, lon1, lat2, lon2):

    # Erdradius in km
    R = 6371.0
    
    # Umwandlung in Bogenma�
    lat1_rad = radians(float(lat1))
    lon1_rad = radians(float(lon1))
    lat2_rad = radians(float(lat2))
    lon2_rad = radians(float(lon2))
    
    # Differenzen
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance


# FIXME: Request does not find itself
def filter_by_radius(base_report: Dict, reports: List[Dict], radius_meters=100) -> List[Dict]:

    base_lat = float(base_report["geolocation_latitude"])
    base_lon = float(base_report["geolocation_longitude"])

    radius_km = radius_meters / 1000.0
    
    matching = []
    for report in reports:
        lat = float(report["geolocation_latitude"])
        lon = float(report["geolocation_longitude"])

        distance = calculate_distance_km(base_lat, base_lon, lat, lon)
        if distance <= radius_km:
            matching.append(report)
    
    return matching



def run(request_id):
    new_request = get_request_dict(request_id)

    result = dublicate_prefilter(new_request)

    # TODO: setze einen Prompt bei der LLM auf, der die potenziellen Duplikate überprüft

    if not result:
        print("No duplicates found.")
        return

    print(f"Found {len(result)} potential duplicates for request {request_id}:")

    # TODO: generiere einen Email Text, der darüber informiert, dass ein neuer Mangel
    #  eingegangen ist (mit der Request ID) und dass es potenzielle Duplikate gibt.
    #  Liste die IDs der potenziellen Duplikate auf.

if __name__ == "__main__":
    new_request = f"#{sys.argv[1]}" # arg: 16773-2025

    run(new_request)
