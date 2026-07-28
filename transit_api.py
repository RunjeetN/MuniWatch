"""511 SF transit data fetching. No UI concerns live here."""

import os
import json
from math import floor
from datetime import datetime, timezone
from collections import defaultdict

import requests
from dateutil.parser import isoparse


API_TOKEN = os.getenv("SF511_API_TOKEN", "fe08bdf9-b21c-42d4-ad23-603f2ef284ef")
AGENCY = "SF"


def calc_minutes_to_arrival(arrival_time: str) -> int:
    """'2026-07-19T20:14:34Z' -> whole minutes from now (may be negative)."""
    dt = isoparse(arrival_time)
    curr_time = datetime.now(timezone.utc)
    return floor((dt - curr_time).total_seconds() / 60)


def get_line_info(stopcode: int) -> defaultdict:
    """Return {line_ref: [minutes_to_arrival, ...]} for a stop. Empty on failure."""
    res = defaultdict(list)
    try:
        response = requests.get(
            "http://api.511.org/transit/StopMonitoring",
            params={
                "api_key": API_TOKEN,
                "agency": AGENCY,
                "stopcode": stopcode,
                "format": "json",
            },
            timeout=10,
        )
        data = json.loads(response.content.decode("utf-8-sig"))
        visits = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    except Exception:
        return res

    for entry in visits:
        journey = entry["MonitoredVehicleJourney"]
        expected = journey["MonitoredCall"]["ExpectedArrivalTime"]
        res[journey["LineRef"]].append(calc_minutes_to_arrival(expected))
    return res
