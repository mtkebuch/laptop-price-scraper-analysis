import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://ultra.ge/%E1%83%9C%E1%83%9D%E1%83%A3%E1%83%97%E1%83%91%E1%83%A3%E1%83%A5%E1%83%94%E1%83%91%E1%83%98"
PRODUCT_LIMIT = 50
MAX_PAGES = 10
MAX_WORKERS = 3
DELAY_SECONDS = 1


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_products_info(limit=PRODUCT_LIMIT, max_pages=MAX_PAGES):
    driver = create_driver()
    products_data = []

    try:
        page = 1
        while len(products_data) < limit and page <= max_pages:
            driver.get(f"{BASE_URL}?page={page}")
            wait = WebDriverWait(driver, 10)
            products = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.thumb-description.clearfix")
            ))

            for p in products:
                if len(products_data) >= limit:
                    break

                link_elem = p.find_element(By.CSS_SELECTOR, "h4.product-title a")
                full_name = link_elem.text
                product_url = link_elem.get_attribute("href")

                if full_name.lower().startswith("ნოუთბუქი") and " " in full_name:
                    name = full_name.split(" ", 1)[1]
                else:
                    name = full_name

                price_block = p.find_element(By.CSS_SELECTOR, "div.price-rating p.price")
                new_price = price_block.find_elements(By.CSS_SELECTOR, "span.price-new")
                old_price = price_block.find_elements(By.CSS_SELECTOR, "span.price-old")

                current_price = new_price[0].text if new_price else price_block.text.strip()
                original_price = old_price[0].text if old_price else current_price

                products_data.append({
                    "name": name,
                    "current_price": current_price,
                    "original_price": original_price,
                    "url": product_url,
                })

            page += 1
            time.sleep(2)

        return products_data
    finally:
        driver.quit()


counter = {"count": 0}


def build_row(product_info, screen_size="", ram="", ssd=""):
    return {
        "Product Name": product_info["name"],
        "Current Price": product_info["current_price"],
        "Original Price": product_info["original_price"],
        "Discounted": "Yes" if product_info["current_price"] != product_info["original_price"] else "No",
        "Screen Size": screen_size,
        "RAM": ram,
        "SSD": ssd,
    }


def get_specs(product_info, total):
    driver = create_driver()
    try:
        time.sleep(DELAY_SECONDS)
        driver.get(product_info["url"])
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-striped")))

        screen_size = ram = ssd = ""
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-striped tr")
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 2:
                label = tds[0].text.strip()
                value = tds[1].text.strip()
                if "ეკრანის ზომა" in label:
                    screen_size = value.replace('"', '')
                elif "ოპერატიული მეხსიერება" in label:
                    ram = value
                elif "SSD მყარი დისკის მოცულობა" in label:
                    ssd = value

        counter["count"] += 1
        print(f"{counter['count']}/{total} - {product_info['name'][:30]}... "
              f"[RAM: {ram or 'N/A'}, SSD: {ssd or 'N/A'}, Screen: {screen_size or 'N/A'}]")

        return build_row(product_info, screen_size, ram, ssd)

    except Exception as e:
        counter["count"] += 1
        print(f"{counter['count']}/{total} - Error: {product_info['name'][:30]} ({type(e).__name__})")
        return build_row(product_info)

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Fetching product list...")
    products = get_products_info()
    total = len(products)
    print(f"Found {total} products\n")

    print(f"Fetching product details (parallel, {MAX_WORKERS} threads)...\n")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(lambda p: get_specs(p, total), products))

    df = pd.DataFrame(results)
    df.to_excel("ultra_prices_50.xlsx", index=False)

    ram_count = sum(1 for d in results if d["RAM"])
    ssd_count = sum(1 for d in results if d["SSD"])
    screen_count = sum(1 for d in results if d["Screen Size"])

    print(f"\nCompleted: {len(df)} products")
    print(f"   RAM found: {ram_count}/{len(df)}")
    print(f"   SSD found: {ssd_count}/{len(df)}")
    print(f"   Screen found: {screen_count}/{len(df)}")