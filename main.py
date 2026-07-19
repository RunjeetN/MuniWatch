import requests
import json
from datetime import datetime, timezone
from dateutil.parser import isoparse
from math import floor
from collections import defaultdict

# setup API
API_TOKEN = "fe08bdf9-b21c-42d4-ad23-603f2ef284ef"
AGENCY = "SF"
EASTBOUND_STOPCODE = 15419
WESTBOUND_STOPCODE = 16996


response = requests.get(f'http://api.511.org/transit/StopMonitoring?api_key={api_token}&agency={agency_id}&stopcode={eastbound_stopcode}&format=json')

def calc_minutes_to_arrival(arrival_time: str) -> int:
    # input: 2026-07-19T20:14:34Z
    dt = isoparse(arrival_time)
    curr_time = datetime.now(timezone.utc)
    diff = floor(((dt - curr_time).total_seconds()) / 60)
    return diff

def getLineInfo(stopcode: int) -> None:
    res = defaultdict(list)
    data = json.loads(response.content.decode('utf-8-sig'))

    lines = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    for entry in lines:
        journeyInfo = entry["MonitoredVehicleJourney"]
        expected_arrival_time = entry["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        line_name = journeyInfo["LineRef"]
        res[line_name].append(calc_minutes_to_arrival(expected_arrival_time))
    return res 
    


east_bound_info = getLineInfo(eastbound_stopcode)
print(east_bound_info)
