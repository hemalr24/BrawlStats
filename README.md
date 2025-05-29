# BrawlStats

This Python app uses the [Brawl Stars API](https://developer.brawlstars.com/) to fetch and track your recent battles and brawler trophy history. It stores the data persistently and generates an interactive graph to visualize trophy progression over time for selected brawlers.

---

## Features

- Connects to the official Brawl Stars API using your player tag.
- Retrieves and stores recent battles without duplicating existing data.
- Tracks trophies earned by each brawler in matches you've played.
- Saves all historical match data in a CSV file (`brawler_battles.csv`).
- Generates an interactive, toggleable line chart (`brawler_trophies_plot.html`) showing trophy progression for multiple brawlers.
- Lets you filter brawlers dynamically by name for focused analysis.