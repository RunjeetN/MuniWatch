# setup API
api_token = "fe08bdf9-b21c-42d4-ad23-603f2ef284ef"
agency_id = "SF"
eastbound_stopcode = 15419
westbound_stopcode = 16996

import requests 
import json


response = requests.get(f'http://api.511.org/transit/StopMonitoring?api_key={api_token}&agency={agency_id}&stopcode={eastbound_stopcode}&format=json')



def getLineInfo(stopcode: int) -> None:
    res = []
    data = json.loads(response.content.decode('utf-8-sig'))

    lines = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    for entry in lines:
        journeyInfo = entry["MonitoredVehicleJourney"]
        expected_arrival_time = entry["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        line_name = journeyInfo["LineRef"]
        res.append([line_name, expected_arrival_time])
    return res 
    #print(json.dumps(line, indent=4))


east_bound_info = getLineInfo(eastbound_stopcode)
print(east_bound_info)
