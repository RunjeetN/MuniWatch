import requests
import json
from datetime import datetime, timezone
from dateutil.parser import isoparse
from math import floor
from collections import defaultdict, deque
import pandas as pd
import streamlit as st


API_TOKEN = "fe08bdf9-b21c-42d4-ad23-603f2ef284ef"
AGENCY = "SF"
EASTBOUND_STOPCODE = 15419
WESTBOUND_STOPCODE = 16996
IMAGE_PATH_MAPPINGS = {'J': 'assets/J_Church_logo.svg', 
                       'Van Ness': 'assets/BSicon_BUS3.svg',
                       'E': 'assets/E_Embarcadero_logo.svg',
                       'F': 'assets/F_Market_&_Wharves_logo.svg',
                       'K': 'assets/K_Ingleside_logo.svg',
                       'M': 'assets/M_Ocean_View_logo.svg',
                       'N': 'assets/N_Judah_logo.svg',
                       'S': 'assets/S_Shuttle_logo.svg',
                       'T': 'assets/T_Third_Street_logo.svg',
                       'L': 'assets/L_Taraval_logo.svg'}


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

def big(n):
    st.markdown(
        f"<p style='font-size:64px; font-weight:700; text-align:center; margin:0'>{n}</p>",
        unsafe_allow_html=True,
    )

def build_row(row_data: tuple, parent, unique_key:str):
    """
    create and populate row container
    example row_data: ('N': [0, 17, 29])
    parent: eastbound or westbound containers 
    """
    image_col, value1_col, value2_col, value3_col = parent.columns([1.5, 1, 1, 1])
    
    line, times = row_data
    with image_col:
        st.image(image=IMAGE_PATH_MAPPINGS[line])
            
    cols = [value1_col, value2_col, value3_col]
    for col, t in zip(cols, times):
        with col:
            big(t)
    
def build_table(data: defaultdict, parent_container, key:str):
    with parent_container:
        st.title(key, text_alignment="center")
    for row in data.items():
        build_row(row, parent_container, key)

def run():
    st.set_page_config(layout="wide")

    eastbound_info = getLineInfo(EASTBOUND_STOPCODE)
    westbound_info = getLineInfo(WESTBOUND_STOPCODE)

    with st.container(border=True, horizontal=True, width="stretch"):
        # eastbound
        build_table(eastbound_info, st.container(border=True, width="stretch", horizontal_alignment="center", vertical_alignment="center"), key="East")
        # westbound 
        build_table(westbound_info, st.container(border=True, width="stretch", horizontal_alignment="center", vertical_alignment="center"), key="West")



run()