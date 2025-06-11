import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.squareyards.com/resale/property-in-mumbai-for-sale"  # Example resale property listings

print("🚀 Opening page...")
driver.get(url)
time.sleep(5)  # Wait for dynamic content to load

print("🔍 Scraping listings...")
listings = driver.find_elements(By.CLASS_NAME, "cardWrap___vJ3zv")  # This class may need update

data = []
for listing in listings:
    try:
        title = listing.find_element(By.CLASS_NAME, "srpCard__title___Qxy5i").text
        price = listing.find_element(By.CLASS_NAME, "srpCard__price___f7oqL").text
        location = listing.find_element(By.CLASS_NAME, "srpCard__address___HJ5Bb").text
        data.append([title, price, location])
    except Exception:
        continue

driver.quit()

# Save to CSV
if data:
    import os
    os.makedirs("output", exist_ok=True)
    with open("output/listings.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Location"])
        writer.writerows(data)
    print(f"✅ Scraped {len(data)} listings to output/listings.csv")
else:
    print("⚠️ No listings found. Structure may have changed.")