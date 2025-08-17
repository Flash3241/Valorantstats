# Valorantstats

Tool for scraping and analyzing Valorant player stats from [vlr.gg](https://www.vlr.gg/).  
Collects the last 5 games of a chosen player’s kills and calculates their probability of clearing a custom kill line.

---

## 🎯 Features
- Scrapes match data for any Valorant player from vlr.gg
- Collects kill counts from the last 5 games
- Calculates **hit rate probability** of clearing a user-defined kill line
- Displays average kills and confidence intervals for better insights
- Simple CLI prompts for player name and target line

---

## ⚠️ Disclaimer
This project is intended for **educational and personal-use purposes only**.  
Use responsibly and in compliance with [vlr.gg](https://www.vlr.gg/) terms of service.  

---

## 🛠 Requirements
- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (must match your Chrome version)

---

## 🔧 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/Flash3241/Valorantstats.git
   cd Valorantstats
