# Real Estate Web Scraper (Python)

A lightweight Python automation tool that scrapes apartment listings, current prices, and locations from real estate portals and saves them into a structured CSV format.

## Features
- Fetches real-time real estate data.
- Parses HTML structures using **BeautifulSoup4**.
- Handles Czech diacritics smoothly (exports with UTF-8-SIG encoding for perfect Excel compatibility).
- Implements custom `User-Agent` headers to mimic human behavior and prevent request blocking.

## Tech Stack
- **Python 3**
- **Requests** (HTTP communication)
- **BeautifulSoup4** (HTML parsing)
- **CSV & RegEx** (Data processing and storage)

## How to run
1. Install dependencies: `pip install requests beautifulsoup4`
2. Run the script: `python scraper.py`
3. Check the generated `reality_vystup.csv` file.
