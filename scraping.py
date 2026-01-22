from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_products_info():
    driver = create_driver()
    url = "https://ultra.ge/%E1%83%9C%E1%83%9D%E1%83%A3%E1%83%97%E1%83%91%E1%83%A3%E1%83%A5%E1%83%94%E1%83%91%E1%83%98?limit=50"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        products = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.thumb-description.clearfix")
        ))

        products_data = []
        for p in products[:50]:
            link_elem = p.find_element(By.CSS_SELECTOR, "h4.product-title a")
            full_name = link_elem.text
            product_url = link_elem.get_attribute("href")

            name = full_name.split(" ", 1)[1] if full_name.lower().startswith("ნოუთბუქი") and " " in full_name else full_name

            price_block = p.find_element(By.CSS_SELECTOR, "div.price-rating p.price")
            current_price = price_block.find_element(By.CSS_SELECTOR, "span.price-new").text if len(price_block.find_elements(By.CSS_SELECTOR, "span.price-new")) > 0 else price_block.text.strip()
            original_price = price_block.find_element(By.CSS_SELECTOR, "span.price-old").text if len(price_block.find_elements(By.CSS_SELECTOR, "span.price-old")) > 0 else current_price

            products_data.append({
                "name": name,
                "current_price": current_price,
                "original_price": original_price,
                "url": product_url
            })

        return products_data
    finally:
        driver.quit()

counter = {"count": 0}

def get_specs(product_info):
    driver = create_driver()
    try:
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
        print(f"{counter['count']}/50 - {product_info['name'][:30]}... [RAM: {ram or 'N/A'}, SSD: {ssd or 'N/A'}, Screen: {screen_size or 'N/A'}]")

        return {
            "Product Name": product_info["name"],
            "Current Price": product_info["current_price"],
            "Original Price": product_info["original_price"],
            "Discounted": "Yes" if product_info["current_price"] != product_info["original_price"] else "No",
            "Screen Size": screen_size,
            "RAM": ram,
            "SSD": ssd
        }
    except:
        counter["count"] += 1
        print(f"{counter['count']}/50 - Error: {product_info['name'][:30]}")
        return {
            "Product Name": product_info["name"],
            "Current Price": product_info["current_price"],
            "Original Price": product_info["original_price"],
            "Discounted": "Yes" if product_info["current_price"] != product_info["original_price"] else "No",
            "Screen Size": "",
            "RAM": "",
            "SSD": ""
        }
    finally:
        driver.quit()

print("Fetching product list...")
products = get_products_info()
print(f"Found {len(products)} products\n")

print("Fetching product details (parallel, 10 threads)...\n")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(get_specs, products))

df = pd.DataFrame(results)
df.to_excel("ultra_prices_50.xlsx", index=False)

ram_count = sum(1 for d in results if d["RAM"])
ssd_count = sum(1 for d in results if d["SSD"])
screen_count = sum(1 for d in results if d["Screen Size"])

print(f"\nCompleted: {len(df)} products")
print(f"   RAM found: {ram_count}/{len(df)}")
print(f"   SSD found: {ssd_count}/{len(df)}")
print(f"   Screen found: {screen_count}/{len(df)}")
