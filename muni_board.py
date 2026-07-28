"""Streamlit departure-board UI. All styling and rendering lives here."""

import os
import base64
from collections import defaultdict

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from transit_api import get_line_info


EASTBOUND_STOPCODE = 15419
WESTBOUND_STOPCODE = 16996

IMAGE_PATH_MAPPINGS = {
    'J': 'assets/J_Church_logo.svg',
    'Van Ness': 'assets/BSicon_BUS3.svg',
    'E': 'assets/E_Embarcadero_logo.svg',
    'F': 'assets/F_Market_&_Wharves_logo.svg',
    'K': 'assets/K_Ingleside_logo.svg',
    'M': 'assets/M_Ocean_View_logo.svg',
    'N': 'assets/N_Judah_logo.svg',
    'S': 'assets/S_Shuttle_logo.svg',
    'T': 'assets/T_Third_Street_logo.svg',
    'L': 'assets/L_Taraval_logo.svg',
}


@st.cache_data
def _svg_data_uri(path: str):
    if not path or not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/svg+xml;base64,{b64}"


def badge_html(line: str) -> str:
    uri = _svg_data_uri(IMAGE_PATH_MAPPINGS.get(line, ""))
    if uri:
        return f"<img class='logo' src='{uri}' alt='{line}'/>"
    return f"<span class='logo logo-fallback'>{line}</span>"


def board_html(data: defaultdict, title: str, arrow: str) -> str:
    rows = []
    for line, times in sorted(data.items(), key=lambda kv: min(kv[1], default=999)):
        chips = []
        for i, t in enumerate(sorted(times)[:4]):
            cls = "time next" if i == 0 else "time later"
            if t <= 0:
                chips.append(f"<div class='{cls}'>Now</div>")
            else:
                chips.append(f"<div class='{cls}'>{t}<span class='unit'>min</span></div>")
        rows.append(
            f"<div class='row'><div class='badge'>{badge_html(line)}</div>"
            f"<div class='times'>{''.join(chips)}</div></div>"
        )
    if not rows:
        rows.append("<div class='empty'>No upcoming arrivals</div>")

    return (
        f"<div class='board'>"
        f"<div class='board-head'><span class='arrow'>{arrow}</span>{title}</div>"
        f"{''.join(rows)}</div>"
    )


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp { background: #0b0f14; }
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

.title { font-family:'Inter',sans-serif; color:#e8edf3; font-weight:800;
         font-size:26px; letter-spacing:.5px; text-align:center; margin-bottom:1.2rem; }

.board { background:#12171f; border:1px solid #222c38; border-radius:18px;
         padding:20px 22px; height:100%; font-family:'Inter',sans-serif; }
.board-head { color:#8a97a8; text-transform:uppercase; letter-spacing:2px;
              font-size:14px; font-weight:700; padding-bottom:14px; margin-bottom:6px;
              border-bottom:1px solid #222c38; display:flex; align-items:center; gap:8px; }
.arrow { color:#ffc255; font-size:16px; }

.row { display:flex; align-items:center; gap:16px; padding:14px 4px;
       border-bottom:1px solid #1a222c; }
.row:last-child { border-bottom:none; }

.badge { flex:0 0 56px; display:flex; align-items:center; justify-content:center; }
.logo { width:48px; height:48px; object-fit:contain; }
.logo-fallback { width:48px; height:48px; border-radius:50%; background:#2a3441;
                 color:#e8edf3; font-weight:800; display:flex; align-items:center;
                 justify-content:center; font-size:18px; }

.times { display:flex; align-items:baseline; gap:22px; margin-left:auto; }
.time { font-variant-numeric:tabular-nums; line-height:1; }
.next { color:#ffc255; font-size:46px; font-weight:800; }
.later { color:#6f7d8c; font-size:24px; font-weight:600; }
.unit { font-size:14px; font-weight:600; margin-left:3px; opacity:.75; }

.empty { color:#4d5763; text-align:center; padding:28px 0; font-size:15px; }
</style>
"""


def run():
    st.set_page_config(layout="wide", page_title="Muni Arrivals")
    st.markdown(CSS, unsafe_allow_html=True)
    st_autorefresh(interval=180_000, key="refresh")  # 3 min

    st.markdown("<div class='title'>Muni Metro — Live Arrivals</div>", unsafe_allow_html=True)

    eastbound = get_line_info(EASTBOUND_STOPCODE)
    westbound = get_line_info(WESTBOUND_STOPCODE)

    left, right = st.columns(2, gap="large")
    with right:
        st.markdown(board_html(eastbound, "Eastbound", "▸"), unsafe_allow_html=True)
    with left:
        st.markdown(board_html(westbound, "Westbound", "◂"), unsafe_allow_html=True)


run()
