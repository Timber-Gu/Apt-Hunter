from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ----------------- CONFIG -----------------
TARGET_URL = "https://www.apartments.com/seattle-wa/"
MAX_PRICE = 1600
BED_KEYWORDS = ["Studio", "studio", "1 bed"]
MAX_PAGES = 12  # 要爬的最大页数

SCROLL_TIMES = 8
SCROLL_PAUSE = 2
# -----------------------------------------

def scroll_to_bottom(driver, scroll_times=15, pause=2):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

def extract_min_price(price_text):
    numbers = re.findall(r"\$[\d,]+", price_text)
    if numbers:
        min_price = int(numbers[0].replace("$", "").replace(",", ""))
        return min_price
    return None

def get_apartment_data(base_url, max_pages=5):
    options = Options()
    # 可打开这行观察浏览器窗口（反爬调试时很有用）
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    apartments = []

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url.rstrip('/')}/{page}/"
        print(f"\n📄 抓取第 {page} 页: {url}")
        driver.get(url)
        scroll_to_bottom(driver, scroll_times=SCROLL_TIMES, pause=SCROLL_PAUSE)

        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "placard")))
        except:
            print(f"⚠️ 第 {page} 页加载失败，跳过")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.find_all("article", class_="placard")
        print(f"✅ 找到 {len(listings)} 条房源")

        for apt in listings:
            a_tag = apt.find("a", class_="property-link")
            name = a_tag.get("aria-label") if a_tag else "N/A"
            link = a_tag.get("href") if a_tag else "N/A"

            price_tag = apt.find("p", class_="property-pricing")
            bed_tag = apt.find("p", class_="property-beds")
            addr_tag = apt.find("div", class_="property-address")

            price_text = price_tag.text.strip() if price_tag else ""
            bed_text = bed_tag.text.strip().lower() if bed_tag else ""
            address = addr_tag.text.strip() if addr_tag else ""

            min_price = extract_min_price(price_text)

            if not any(key in bed_text for key in BED_KEYWORDS):
                continue
            if min_price is None or min_price > MAX_PRICE:
                continue

            apartments.append({
                "名称": name,
                "链接": link,
                "价格": price_text,
                "卧室": bed_text,
                "地址": address
            })

    driver.quit()
    print(f"\n📦 共筛选出 {len(apartments)} 条房源")
    return apartments

def save_to_excel(apartments, filename="apartments_unclassified.xlsx"):
    df = pd.DataFrame(apartments)
    df.to_excel(filename, index=False)
    print(f"✅ 已保存至文件：{filename}")


if __name__ == "__main__":
    apartments = get_apartment_data(TARGET_URL, max_pages=MAX_PAGES)
    save_to_excel(apartments)




