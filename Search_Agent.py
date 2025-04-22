from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# ----------------- CONFIG -----------------
# Base URL for apartment search
TARGET_URL = "https://www.apartments.com/seattle-wa/"
# Maximum price filter for apartments
MAX_PRICE = 1600
# Keywords to filter bedroom types
BED_KEYWORDS = ["Studio", "studio", "1 bed"]
# Maximum number of pages to scrape
MAX_PAGES = 12

# Scroll configuration
SCROLL_TIMES = 8
SCROLL_PAUSE = 2
# -----------------------------------------

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('apartment_scraper.log')
    ]
)

def validate_config():
    """Validate configuration parameters."""
    if not TARGET_URL.startswith("https://"):
        raise ValueError("TARGET_URL must be a valid HTTPS URL")
    if MAX_PRICE <= 0:
        raise ValueError("MAX_PRICE must be greater than 0")
    if MAX_PAGES <= 0:
        raise ValueError("MAX_PAGES must be greater than 0")
    if not BED_KEYWORDS:
        raise ValueError("BED_KEYWORDS cannot be empty")

def scroll_to_bottom(driver, scroll_times=15, pause=2):
    """
    Scroll the page to load dynamic content.
    
    Args:
        driver: Selenium WebDriver instance
        scroll_times: Number of scroll attempts
        pause: Time to pause between scrolls
    """
    for i in range(scroll_times):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
        except WebDriverException as e:
            logging.error(f"Error during scroll attempt {i+1}: {str(e)}")

def extract_min_price(price_text):
    """
    Extract the minimum price from price text.
    
    Args:
        price_text: String containing price information
    
    Returns:
        int: Minimum price if found, None otherwise
    """
    if not price_text:
        return None
    
    numbers = re.findall(r"\$[\d,]+", price_text)
    if numbers:
        try:
            min_price = int(numbers[0].replace("$", "").replace(",", ""))
            return min_price
        except ValueError:
            logging.warning(f"Could not parse price from: {price_text}")
            return None
    return None

def get_apartment_data(base_url, max_pages=5):
    """
    Scrape apartment listings from the website.
    
    Args:
        base_url: Base URL to scrape
        max_pages: Maximum number of pages to scrape
    
    Returns:
        list: List of dictionaries containing apartment information
    """
    validate_config()
    options = Options()
    # Uncomment to run in headless mode
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        logging.error(f"Failed to initialize Chrome driver: {str(e)}")
        return []

    apartments = []
    
    try:
        for page in range(1, max_pages + 1):
            url = base_url if page == 1 else f"{base_url.rstrip('/')}/{page}/"
            logging.info(f"Scraping page {page}: {url}")
            
            try:
                driver.get(url)
                scroll_to_bottom(driver, scroll_times=SCROLL_TIMES, pause=SCROLL_PAUSE)

                # Wait for listings to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "placard"))
                )
            except TimeoutException:
                logging.warning(f"Page {page} timed out, skipping")
                continue
            except WebDriverException as e:
                logging.error(f"Error loading page {page}: {str(e)}")
                continue

            soup = BeautifulSoup(driver.page_source, "html.parser")
            listings = soup.find_all("article", class_="placard")
            logging.info(f"Found {len(listings)} listings on page {page}")

            for apt in listings:
                try:
                    apartment = parse_apartment_listing(apt)
                    if apartment:
                        apartments.append(apartment)
                except Exception as e:
                    logging.error(f"Error parsing listing: {str(e)}")
                    continue

    except Exception as e:
        logging.error(f"Unexpected error during scraping: {str(e)}")
    finally:
        driver.quit()

    logging.info(f"Successfully filtered {len(apartments)} apartments")
    return apartments

def parse_apartment_listing(apt):
    """
    Parse individual apartment listing.
    
    Args:
        apt: BeautifulSoup object containing apartment listing
    
    Returns:
        dict: Apartment information if it matches criteria, None otherwise
    """
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

    if not any(key.lower() in bed_text.lower() for key in BED_KEYWORDS):
        return None
    if min_price is None or min_price > MAX_PRICE:
        return None

    return {
        "name": name,
        "link": link,
        "price": price_text,
        "bedrooms": bed_text,
        "address": address
    }

def save_to_excel(apartments, filename="apartments.xlsx"):
    """
    Save apartment data to Excel file.
    
    Args:
        apartments: List of apartment dictionaries
        filename: Output Excel filename
    """
    if not apartments:
        logging.warning("No apartments to save")
        return

    try:
        df = pd.DataFrame(apartments)
        df.to_excel(filename, index=False)
        logging.info(f"Successfully saved to file: {filename}")
    except Exception as e:
        logging.error(f"Error saving to Excel: {str(e)}")

if __name__ == "__main__":
    try:
        apartments = get_apartment_data(TARGET_URL, max_pages=MAX_PAGES)
        save_to_excel(apartments)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")




