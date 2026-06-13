import time, re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

IMDB_TOP250_URL = "https://www.imdb.com/chart/top/"

def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
    return driver

def main():
    driver = create_driver()
    try:
        driver.get(IMDB_TOP250_URL)
        time.sleep(10)
        for _ in range(20):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.4)
        time.sleep(3)
        items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        print("===== RAW TEXT OF FIRST 3 ITEMS =====")
        for i in range(min(3, len(items))):
            print(f"\n--- ITEM {i} ---")
            print(repr(items[i].text))
        print("=====================================")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
