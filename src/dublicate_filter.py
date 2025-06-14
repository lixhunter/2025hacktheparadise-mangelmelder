import json
import os
import sys
import datetime
import re
from typing import List, Dict


new_request = f"#{sys.argv[1]}"


def dublicate_prefilter(newReport:  Dict) -> List[Dict]:
    # reportsList = API call --> alle reports holen
    # recentReports = filter_by_timeSpan(entries)
    # nearRecentReports = filter_by_radius(newReport, recentReports)

    # return nearRecentReports
    return None

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
    
    # Umwandlung in Bogenmaß
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
