# setup API
api_token = "fe08bdf9-b21c-42d4-ad23-603f2ef284ef"
agency_id = "SF"
eastbound_stopcode = 15419
westbound_stopcode = 16996

import requests 
import json


response = requests.get(f'http://api.511.org/transit/StopMonitoring?api_key={api_token}&agency={agency_id}&format=json')

data = json.loads(response.content.decode('utf-8-sig'))

visits = (data["ServiceDelivery"]
              ["StopMonitoringDelivery"]
              ["MonitoredStopVisit"])   # this is a list

for v in visits:
    journey = v["MonitoredVehicleJourney"]
    line = journey["LineRef"]                                  # e.g. "J"
    arrival = journey["MonitoredCall"]["ExpectedArrivalTime"]
    print(f'journey: {journey}\nline: {line}\narrival: {arrival}')

