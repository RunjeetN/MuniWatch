# Muni Metro Live Arrivals

A real-time departure board for SF Muni Metro, built with [Streamlit](https://streamlit.io). It shows upcoming eastbound and westbound arrivals for a pair of stops, styled like a transit terminal display and auto-refreshing every few minutes.

Data comes from the [511 SF Bay Open Data API](https://511.org/open-data).

## Features

- Live arrival times for two directions, side by side
- Official Muni line logos, with a lettered fallback badge if an asset is missing
- Next arrival highlighted; following arrivals dimmed, all labeled in minutes (`Now` when a train is due)
- Auto-refreshes every 3 minutes
- Backend data logic is decoupled from the UI, so the API layer can be reused or tested on its own

## Project structure

```
.
├── muni_board.py      # Streamlit app: styling, layout, rendering
├── transit_api.py     # Backend: 511 API fetching and time calculation
├── requirements.txt   # Python dependencies
└── assets/            # Muni line logo SVGs
```

## Prerequisites

- Python 3.9+
- A free 511 API token — request one at https://511.org/open-data/token

## Setup

1. Clone the repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Provide your 511 API token via an environment variable (do **not** hardcode it):

   ```bash
   export SF511_API_TOKEN="your-token-here"
   ```

3. Run the app:

   ```bash
   streamlit run muni_board.py
   ```

   It opens at http://localhost:8501.

## Configuration

The stops are set at the top of `muni_board.py`:

```python
EASTBOUND_STOPCODE = 15419
WESTBOUND_STOPCODE = 16996
```

To track different stops, replace these with the stop codes you want. Stop codes can be looked up through the 511 API or on stop signage.

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, and click **New app**.
3. Select the repo, branch, and `muni_board.py` as the entry point, then deploy.
4. Add your token under the app's **Settings → Secrets**:

   ```toml
   SF511_API_TOKEN = "your-token-here"
   ```

   Read it in code with `st.secrets["SF511_API_TOKEN"]`, or keep the existing `os.getenv` fallback and set it as an environment variable in the same settings panel.

5. (Optional) Under **Settings → General**, rename the subdomain to get a cleaner URL like `muni-board.streamlit.app`.

## Notes

- The `assets/` folder must be committed to the repo for the line logos to render.
- Keep your API token out of version control. If it has ever been committed, rotate it.

## Dependencies

```
streamlit
streamlit-autorefresh
requests
python-dateutil
```
