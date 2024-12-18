import os
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import config

def rebeelo_good_quality(models):
    try:
        print("Scraping Rebeelo (Good quality)...")
        headers  = {"User-Agent" : "Mozilla/5.0"}
        products = []

        for model in models:
            search_url = f"https://reebelo.com/search?query={model}"
            print(f"Scraping: {search_url}...")

            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            for product in soup.find_all("div", class_="Product_card"):
                quality = product.find("div", class_="quality")
                if quality and "Good" in quality.get_text(strip=True):
                    title = product.find("h2", class_="title").get_text(strip=True) if product.find("h2", class_="title") else "N/A"
                    price = product.find("span", class_="price").get_text(strip=True) if product.find("span", class_="price") else "N/A"
                    link  = product.find("a"), ["href"] if product.find("a") else "N/A"

                    products.append({
                        "Model" : model,
                        "Title" : title,
                        "Price" : price,
                        "Quality" : "Good",
                        "Links" : "https://reebelo.com{link}"
                    })

        return pd.Dataframe(products)

    except Exception as e:
        print(f"Erorr scraping Rebeelo: {e}")
        return pd.DataFrame()

def scrape_backmarket(models):
    try:
        print("Scraping BackMarket (Good quality)")
        headers  = {"User-Agent" : "Mozilla/5.0"}
        products = []

        for model in models:
            search_url = f"https://www.backmarket.com/en-us/search?q={model}"
            print("Scraping: {search_url}...")

            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()

