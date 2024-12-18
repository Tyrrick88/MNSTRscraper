#MNSTRscraper
# Reebelo & BackMarket Scraper for Refurbished Devices

## Overview
This script automates the scraping of refurbished **iPhone** and **Samsung** devices from two platforms:
- **Reebelo**: Fetches devices labeled as *Good Quality*.
- **BackMarket**: Fetches devices tagged as *Staff Picks*.

It dynamically searches for:
- **iPhones** (models iPhone 11 to iPhone 16)
- **Samsung devices** (Galaxy S series, Note series, and A series)

The results are saved in CSV files and emailed daily to a specified recipient.

---

## Features
1. **Dynamic Model Scraping**:
   - Supports iPhones (11 to 16) and all Samsung series.
   - Captures details like **title, price, quality/category**, and **links**.

2. **Automated CSV Generation**:
   - Saves data to timestamped CSV files.

3. **Email Integration**:
   - Sends daily reports with attached CSV files.

4. **Error Handling**:
   - Manages network errors, file saving issues, and invalid responses gracefully.

5. **Daily Scheduling**:
   - Automatically runs every morning at a user-defined time using the `schedule` library.

---

## Prerequisites
Install the required Python libraries:
```bash
pip install requests beautifulsoup4 pandas schedule

