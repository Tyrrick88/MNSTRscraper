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
import schedule




# A function for scraping Rebeelo.com
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
                        "Model"   : model,
                        "Title"   : title,
                        "Price"   : price,
                        "Quality" : "Good",
                        "Links"   : "https://reebelo.com{link}"
                    })

        return pd.Dataframe(products)

    except Exception as e:
        print(f"Erorr scraping Rebeelo: {e}")
        return pd.DataFrame()
# A function for scraping backmarket.com
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

            soup = BeautifulSoup(response.content, "html.parser")

            for product in soup.find_all("div", class_="Product-card"):
                quality = product.find("div", class_="quality")
                if quality and "Good" in quality.get_text(strip=True):
                    title = product.find("h2", class_="title").get_text(strip=True) if product.find("h2", class_="title") else "N/A"
                    price = product.find("span", class_="price").get_text(strip=True) if product.find("span", class_="price") else "N/A"
                    link  = product.find("a"),["href"] if product.find("a")["href"] else "N/A"

                    products.append({
                        "Title"   : title,
                        "Price"   : price,
                        "Quality" : "Good",
                        "Link"    : f"https://www.backmarket.com{link}"
                    })
            return pd.Dataframe(products)

    except Exception as e:
        print(f"Scraping BackMarket (Good quality): {e}")
        return pd.Dataframe()


# Saving te data from the sites in csv's
def save_to_csv(df, full_catalogue):
    try:
        if not df.empty:
            df.to_csv(full_catalogue, index=False)
            print(f"Data saves to {full_catalogue}")
        else:
            print(f"No data to save")
    except Exception as e:
        print(f"Error saving data: {e}")

# Sending the emails
def send_email(subject, body, file_path):
    try;
        print(f"Sending email with {file_path}...")
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject


        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; full_catalogue={os.path.basename(file_path)}")
            msg.attach(part)


        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully: {file_path}")

    except Exception as e:
            print(f"Error sending email: {e}")



# Main Function
def main():
    print("Starting scraping process...")
    iphone_models = [f"iPhone {i}" for i in range(11, 16)]  # iPhone 11 to iPhone 16
    samsung_models = [f"Samsung Galaxy S{i}" for i in range(10, 24)] + ["Samsung Note", "Samsung Galaxy A"]  # Extend as needed
    all_models = iphone_models + samsung_models

    today = datetime.now().strftime("%Y-%m-%d")
    reebelo_file = f"Rebeelo{today}.csv"
    backmarket_file = f"Backmarket{today}.csv"


    try:
        # Reebelo
        reebelo_data = rebeelo_good_quality(all_models)
        save_to_csv(reebelo_data, reebelo_file)
        send_email(
            subject="Reebelo - Good Quality Products",
            body="Attached is the list of Good Quality products from Reebelo.",
            file_path=reebelo_file
        )

        # BackMarket
        backmarket_data = scrape_backmarket(all_models)
        save_to_csv(backmarket_data, backmarket_file)
        send_email(
            subject="BackMarket - Staff Picks",
            body="Attached is the list of Staff Picks from BackMarket.",
            file_path=backmarket_file
        )

        print("Process completed successfully!")

    except Exception as e:
        print(f"Error in main process: {e}")


# Scheduler
schedule.every().day.at(RUN_TIME).do(main)

if __name__ == "__main__":
    print(f"Scheduler started. Script will run every day at {RUN_TIME}.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            print("Script stopped by user.")
            break
        except Exception as e:
            print(f"Scheduler error: {e}")