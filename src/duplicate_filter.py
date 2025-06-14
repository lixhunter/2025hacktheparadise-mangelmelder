import json
import os
import sys
import datetime
import re
from typing import List, Dict
from math import radians, sin, cos, atan2, sqrt

from src.generate_with_llama3 import generate_with_llama3

new_request = f"#{sys.argv[1]}"
global_radius_meters = 300
global_days = 14
global_similarity_threshold = 0.65

def get_request_dict(request_id):
    req_dict: dict

    print(request_id[1:])
    with open(f"../data/cloud-jena/maengel/{request_id[1:]}.json", "r") as file:
        req_dict = json.load(file)

    return req_dict


def duplicate_prefilter(newReport: Dict) -> List[Dict]:
    directory = "../data/cloud-jena/maengel"

    files = [f for f in os.listdir(directory) if f.endswith('.json')]

    reports = []
    for fname in files:
        with open(os.path.join(directory, fname), "r", encoding='utf-8') as f:
            report = json.load(f)
            reports.append(report)

    recent_reports = filter_by_timeSpan(reports)

    near_reports = filter_by_radius(newReport, recent_reports,
                                    radius_meters=global_radius_meters)

    return near_reports


def extract_datetime(text) -> datetime.datetime:
    match = re.search(r'datetime=\"([^\"]+)\"', text)
    if match:
        return datetime.datetime.fromisoformat(match.group(1))
    return None


def filter_by_timeSpan(entries: List[Dict]) -> List[Dict]:
    now = datetime.datetime.now(datetime.timezone.utc)
    two_months_ago = now - datetime.timedelta(days=global_days)

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

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def filter_by_radius(base_report: Dict, reports: List[Dict],
                     radius_meters=100) -> List[Dict]:
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


def similarity_score(param, param1) -> float:
    """Calculate a similarity score between two strings.
    :returns: similarity score between 0 and 1
    """
    prompt = f"Bewerte ob die folgenden beiden Texte den gleichen Mangel beschreiben:\n\n" \
             f"Text 1: \n\"\"\"{param}\n\"\"\"\n\n" \
             f"Text 2: \n\"\"\"{param1}\n\"\"\"\n\n" \
             f"Gib einen Float-Wert zwischen 0 und 1 zurück, wobei 0 keine Beziehung und 1 das gleiche Problem beschreibt.\n" \
             f"Wenn die Texte inhaltlich identisch oder nahezu identisch sind, gib immer 1.0 zurück.\n" \
             f"Beispiel:\n" \
             f"Text 1: \"Die Lampe ist defekt.\"\n" \
             f"Text 2: \"Die Lampe ist defekt.\"\n" \
             f"Antwort: 1.0\n\n" \
             f"Antworte nur mit der Float-Zahl, ohne Kommentare.\n"

    result = generate_with_llama3(prompt)
    #print (f"Similarity score prompt: {prompt}")
    result_float = float(result.strip())
    #print (f"Similarity score result: {result_float}")
    return result_float if 0 <= result_float <= 1 else 0.0


def run(request_id):
    new_request = get_request_dict(request_id)

    prefiltered = duplicate_prefilter(new_request)

    duplicates = [{"score": similarity_score(new_request["description"],
                                            result["description"]),
                    "id": result["title"][1:]} for result in prefiltered]

    filtered_duplicates = [
        dup for dup in duplicates if dup["score"] > global_similarity_threshold
    ]

    sorted_duplicates = sorted(filtered_duplicates, key=lambda x: x["score"],
                               reverse=True)

    top_duplicates = sorted_duplicates[:5]

    print(top_duplicates)

    print(
        f"Found {len(top_duplicates)} potential duplicates for request {request_id}:"
    )

    description = new_request['description']
    description_without_html = re.sub(r'<[^>]*>', '', description)
    message = f"Eine neue Meldung liegt vor:\n{description_without_html}\n"

    if not top_duplicates:
        print(message)
    else:
        duplicate_warning = "Potenzielle Duplikate gefunden:\n" + \
                            "\n".join([item['id'] for item in top_duplicates])
        print(message + duplicate_warning)


if __name__ == "__main__":
    new_request = f"#{sys.argv[1]}"  # arg: 16773-2025

    run(new_request)
