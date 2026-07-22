import requests
import json
from datetime import datetime, timezone
from dateutil.parser import isoparse
from math import floor
from collections import defaultdict, deque
import pandas as pd
import streamlit as st

# setup API
API_TOKEN = "fe08bdf9-b21c-42d4-ad23-603f2ef284ef"
AGENCY = "SF"
EASTBOUND_STOPCODE = 15419
WESTBOUND_STOPCODE = 16996



def calc_minutes_to_arrival(arrival_time: str) -> int:
    # input: 2026-07-19T20:14:34Z
    dt = isoparse(arrival_time)
    curr_time = datetime.now(timezone.utc)
    diff = floor(((dt - curr_time).total_seconds()) / 60)
    return diff

def getLineInfo(stopcode: int) -> defaultdict:
    response = requests.get(f'http://api.511.org/transit/StopMonitoring?api_key={API_TOKEN}&agency={AGENCY}&stopcode={stopcode}&format=json')
    data = json.loads(response.content.decode('utf-8-sig'))
    
    res = defaultdict(list)

    lines = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    for entry in lines:
        journeyInfo = entry["MonitoredVehicleJourney"]
        expected_arrival_time = entry["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        line_name = journeyInfo["LineRef"]
        res[line_name].append(calc_minutes_to_arrival(expected_arrival_time))
    return res 

# convert API dictioanry data to nested list
# example row: (N': [0, 17, 29])
# parent: eastbound or westbound containers 
def build_row(row: tuple, parent, unique_key:str):
    image_col, value1_col, value2_col, value3_col = parent.columns([1.5, 1, 1, 1])
    
    line, times = row
    with image_col:
        st.button(line, key=unique_key+line)
            
    with value1_col:
        st.write(times[0])

    with value2_col:
        st.write(times[1])

    with value3_col:
        st.write(times[2])
    
def build_table(data: defaultdict, parent_container, key:str):
    with parent_container:
        st.title(key, text_alignment="center")
    for row in data.items():
        build_row(row, parent_container, key)

eastbound_info = getLineInfo(EASTBOUND_STOPCODE)
westbound_info = getLineInfo(WESTBOUND_STOPCODE)


with st.container(border=True, horizontal=True):
    # eastbound
    build_table(eastbound_info, st.container(border=True), key="East")
    # westbound 
    build_table(westbound_info, st.container(border=True), key="West")

