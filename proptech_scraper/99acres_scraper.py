from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_99acres():
    url = "https://www.99acres.com/property-in-mumbai-ffid"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"), options=chrome_options)
    driver.get(url)
    time.sleep(5)

    # Scroll to bottom to trigger React lazy loading
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    print("🔍 Scanning for listings...")

    # Use XPath to grab listing wrappers
    cards = driver.find_elements(By.XPATH, "//section[contains(@class,'projectTuple')]")

    print(f"📦 Found {len(cards)} listings.")

    data = []
    for card in cards:
        try:
            title = card.find_element(By.XPATH, ".//a[contains(@class, 'projectTuple__projectName')]").text
        except:
            title = ""
        try:
            location = card.find_element(By.XPATH, ".//div[contains(@class, 'projectTuple__projectSubHeading')]").text
        except:
            location = ""
        try:
            price = card.find_element(By.XPATH, ".//td[contains(@class, 'projectTuple__price')]").text
        except:
            price = ""

        data.append({
            "Title": title,
            "Location": location,
            "Price": price
        })

    driver.quit()

    if data:
        df = pd.DataFrame(data)
        df.to_csv("99acres_mumbai_listings.csv", index=False)
        print("✅ Scraped and saved data to 99acres_mumbai_listings.csv")
    else:
        print("⚠️ No data extracted. Might need to log in or change strategy.")

if __name__ == "__main__":
    scrape_99acres()