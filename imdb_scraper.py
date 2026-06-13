import time, re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

IMDB_TOP250_URL = "https://www.imdb.com/chart/top/"
OUTPUT_FILE = "imdb_top250.csv"

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
    print("[INFO] Starting scraper...")
    driver = create_driver()
    movies = []
    try:
        driver.get(IMDB_TOP250_URL)
        print("[INFO] Waiting for page...")
        time.sleep(10)
        for _ in range(20):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(0.4)
        time.sleep(3)
        items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        print(f"[INFO] Found {len(items)} items. Extracting...")
        for item in items:
            try:
                lines = item.text.strip().split("\n")
                rank = int(lines[0].replace("#", "").strip())
                title = lines[1].strip()
                year_match = re.search(r'(19|20)\d{2}', lines[2]) if len(lines) > 2 else None
                year = year_match.group() if year_match else "N/A"
                rating_match = re.search(r'\d+\.\d+', lines[3]) if len(lines) > 3 else None
                rating = float(rating_match.group()) if rating_match else "N/A"
                movies.append({"rank": rank, "title": title, "year": year, "rating": rating})
                print(f"  [{rank}] {title} ({year}) - {rating}")
            except Exception as e:
                continue
    finally:
        driver.quit()
        print("[INFO] Browser closed.")
    if not movies:
        print("[ERROR] No data scraped.")
        return
    df = pd.DataFrame(movies).sort_values("rank").reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\n[SUCCESS] Saved {len(df)} movies to {OUTPUT_FILE}")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
