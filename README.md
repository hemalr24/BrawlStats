# BrawlStats

This Python app uses the [Brawl Stars API](https://developer.brawlstars.com/) to track and visualize player stats over time, including:

- **Trophy progression per brawler**
- **Overall ranked points history**

The app stores all data persistently and generates interactive graphs for visual analysis.

---

## Features

### 📈 Brawler Trophy Tracker
- Pulls your 25 most recent battles
- Tracks trophies for each brawler used
- Saves all data to `brawler_battles.csv`
- Produces an interactive graph (`brawler_trophies_plot.html`) showing trophy progression for each brawler
- Allows you to dynamically select or toggle brawlers to view

### 🏆 Ranked Points Tracker
- Fetches your current `rankedPoints` from your profile
- Appends the current time and value to `ranked_progress.csv`
- Generates an interactive graph (`ranked_points_plot.html`) showing your ranked points over time

---