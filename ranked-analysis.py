import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objs as go

# Load .env file
load_dotenv()

# Get environment variables
API_KEY = os.getenv("API_KEY")
HEMAL_TAG = os.getenv("HEMAL_TAG")

if not HEMAL_TAG or not API_KEY:
    raise ValueError("Missing API_KEY or HEMAL_TAG in .env file")

# Build API URL with URL-encoded #
url = f"https://api.brawlstars.com/v1/players/%23{HEMAL_TAG}"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Make the request to get player profile
response = requests.get(url, headers=headers)
data = response.json()

# Load existing CSV if it exists
csv_filename = "ranked_progress.csv"
if os.path.exists(csv_filename):
    existing_df = pd.read_csv(csv_filename)
else:
    existing_df = pd.DataFrame()

# Get current timestamp and ranked points
from datetime import datetime
timestamp = datetime.utcnow().isoformat()

ranked_stats = data.get('ranked', {})  # ranked might not exist
ranked_points = ranked_stats.get('rankedPoints', None)

if ranked_points is not None:
    new_row = {
        'timestamp': timestamp,
        'rankedPoints': ranked_points
    }

    # Avoid duplicates based on timestamp
    if not existing_df.empty and timestamp in set(existing_df['timestamp']):
        updated_df = existing_df
    else:
        new_df = pd.DataFrame([new_row])
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_filename, index=False)

    # Plot using Plotly
    updated_df['timestamp'] = pd.to_datetime(updated_df['timestamp'])
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=updated_df['timestamp'],
        y=updated_df['rankedPoints'],
        mode='lines+markers',
        name='Ranked Points'
    ))

    fig.update_layout(
        title="Ranked Points Over Time",
        xaxis_title="Time",
        yaxis_title="Ranked Points",
        hovermode="closest",
        template="plotly_white"
    )

    fig.write_html("ranked_points_plot.html")

else:
    print("Ranked points data is not available for this player.")

