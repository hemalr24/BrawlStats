import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import webbrowser
import plotly.graph_objs as go

load_dotenv()

API_KEY = os.getenv("API_KEY")
HEMAL_TAG = os.getenv("HEMAL_TAG")

if not HEMAL_TAG or not API_KEY:
    raise ValueError("Missing API_KEY or HEMAL_TAG in .env file")

url = f"https://api.brawlstars.com/v1/players/%23{HEMAL_TAG}"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

response = requests.get(url + "/battlelog", headers=headers)
data = response.json()

if 'items' not in data:
    raise ValueError("API response does not contain 'items'. Response was:\n" + json.dumps(data, indent=2))

csv_filename = "brawler_battles.csv"
if os.path.exists(csv_filename):
    existing_df = pd.read_csv(csv_filename)
else:
    existing_df = pd.DataFrame()

new_rows = []
existing_battle_times = set(existing_df['battleTime']) if not existing_df.empty else set()

for battle in data['items']:
    battle_time = battle.get('battleTime')
    if battle_time in existing_battle_times:
        continue  # skip already recorded battles

    player_list = battle.get('battle', {}).get('teams', [[]])[0] + battle.get('battle', {}).get('teams', [[]])[1] if 'teams' in battle.get('battle', {}) else battle.get('battle', {}).get('players', [])

    for player in player_list:
        if player.get('tag', '').lstrip('#') == HEMAL_TAG:
            brawler_info = player.get('brawler', {})
            brawler_name = brawler_info.get('name')
            trophies = brawler_info.get('trophies')
            if brawler_name and trophies is not None:
                new_rows.append({
                    'battleTime': battle_time,
                    'brawler': brawler_name,
                    'trophies': trophies
                })

if new_rows:
    new_df = pd.DataFrame(new_rows)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv(csv_filename, index=False)
else:
    updated_df = existing_df

if not updated_df.empty and 'battleTime' in updated_df.columns:
    updated_df['battleTime'] = pd.to_datetime(updated_df['battleTime'], format="%Y%m%dT%H%M%S.%fZ", errors='coerce')
    updated_df = updated_df.dropna(subset=['battleTime'])
    updated_df = updated_df.sort_values('battleTime')

    fig = go.Figure()

    for brawler in sorted(updated_df['brawler'].unique()):
        brawler_df = updated_df[updated_df['brawler'] == brawler]
        fig.add_trace(go.Scatter(
            x=brawler_df['battleTime'],
            y=brawler_df['trophies'],
            mode='lines+markers',
            name=brawler,
            visible=True
        ))

    fig.update_layout(
        title="Brawler Trophy Progression",
        xaxis_title="Battle Time",
        yaxis_title="Trophies",
        hovermode="closest",
        legend_title="Toggle Brawlers",
        template="plotly_white"
    )

    fig.write_html("brawler_trophies_plot.html")
else:
    print("No valid battle data available.")

webbrowser.open("brawler_trophies_plot.html")