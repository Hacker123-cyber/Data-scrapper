from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import time

def scrape_tokopedia(keyword, page_wait_time=30, csv_file_path="./"):
    """Scrapes product data from Tokopedia and stores it in CSV files by location.

    Args:
        keyword (str): The search term.
        csv_file_path (str, optional): Path to store the CSV files. Defaults to "./".
    """
    driver = webdriver.Chrome()  # Assume Chromedriver setup
    driver.get("https://www.tokopedia.com/")

    try:
        # Use explicit waits for more robust element finding
        search_box = WebDriverWait(driver, page_wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-unify='Search']"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        data_by_location = {}

        # Wait for products to load
        WebDriverWait(driver, page_wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divProductWrapper']"))
        )

        products = driver.find_elements(By.XPATH, "//div[@data-testid='divProductWrapper']")

        for product in products:
            try:
                name_element = product.find_element(By.XPATH, ".//div[@data-testid='spnSRPProdName']")
                name = name_element.text if name_element else None

                location_element = product.find_element(By.XPATH, ".//span[@data-testid='spnSRPProdTabShopLoc']")
                location = location_element.text if location_element else None

                price_element = product.find_element(By.XPATH, ".//div[@data-testid='spnSRPProdPrice']")
                price = price_element.text if price_element else None

                rating_element = product.find_element(By.XPATH, ".//div[contains(@class, 'prd_shop-rating-average-and-label')]/span[1]")
                rating = rating_element.text if rating_element else None

                num_buyers_element = product.find_element(By.XPATH, ".//span[contains(@class, 'prd_label-integrity')]")
                num_buyers = num_buyers_element.text if num_buyers_element else None

                if location not in data_by_location:
                    data_by_location[location] = []

                data_by_location[location].append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Buyers': num_buyers
                })
            except Exception as e:
                print(f"Error processing product: {e}")

        # Write data to CSV files
        for location, products_data in data_by_location.items():
            filename = os.path.join(csv_file_path, f"{location}.csv")
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Name', 'Price', 'Rating', 'Buyers']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products_data)

    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = input("Enter keyword: ")
    scrape_tokopedia(keyword)