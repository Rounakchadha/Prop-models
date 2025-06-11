from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_magicbricks(locality="Andheri", pages=1):
    options = Options()
    options.add_argument("--headless")  # Background browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_listings = []

    for page in range(1, pages + 1):
        url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?locality={locality}&cityName=Mumbai&page={page}"
        print(f"🔍 Visiting: {url}")
        driver.get(url)

        time.sleep(3)  # Give time to load JS

        # DEBUG: Print page source to check if it’s loading
        print("🧪 First 500 characters of page:")
        print(driver.page_source[:500])

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mb-srp__card"))
            )
        except Exception as e:
            print("⚠️ Listings not found or page took too long to load.")
            continue

        cards = driver.find_elements(By.CLASS_NAME, "mb-srp__card")

        for card in cards:
            try:
                title = card.find_element(By.CLASS_NAME, "mb-srp__card--title").text.strip()
                price = card.find_element(By.CLASS_NAME, "mb-srp__card__price--amount").text.strip()
                details = card.find_element(By.CLASS_NAME, "mb-srp__card__summary--value").text.strip()
                all_listings.append({
                    "title": title,
                    "price": price,
                    "details": details
                })
            except:
                continue

        time.sleep(2)  # Pause before next page

    driver.quit()

    df = pd.DataFrame(all_listings)
    df.to_csv("magicbricks_listings.csv", index=False)
    print(f"✅ Scraped {len(df)} listings. Saved to magicbricks_listings.csv.")

if __name__ == "__main__":
    scrape_magicbricks(locality="Andheri", pages=2)