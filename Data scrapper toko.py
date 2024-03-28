from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

def scrape_tokopedia(keyword):
    driver = webdriver.Chrome(r'C:\path\to\chromedriver.exe')  # Update path to your chromedriver
    driver.get("https://www.tokopedia.com/")
    time.sleep(2)  # Wait for page to load

    # Find and input the search box
    search_box = driver.find_element_by_xpath('//input[@name="q"]')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for search results to load

    # Initialize dictionaries to store data
    data_by_category = {}

    # Extract data from search results
    products = driver.find_elements_by_xpath('//div[@class="css-1g20a2m"]')
    for product in products:
        try:
            name = product.find_element_by_xpath('.//span[@class="css-o5uqvq"]').text
            category = product.find_element_by_xpath('.//div[@class="css-1g3cq9l"]').text
            price = product.find_element_by_xpath('.//span[@class="css-ooyzua"]').text
            rating = product.find_element_by_xpath('.//span[@class="css-7fmtuv"]').text
            num_buyers = product.find_element_by_xpath('.//span[@class="css-1bjwylw"]').text

            # Add product data to the corresponding category dictionary
            if category not in data_by_category:
                data_by_category[category] = []
            data_by_category[category].append({'Name': name, 'Price': price, 'Rating': rating, 'Buyers': num_buyers})
        except Exception as e:
            print(f"Error processing product: {e}")

    # Write data to CSV files based on categories
    for category, products_data in data_by_category.items():
        csv_file_path = f"C:/Users/allessandro/Desktop/Startup/{category}.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating', 'Buyers']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product_data in products_data:
                writer.writerow(product_data)

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    keyword = input("Enter keyword: ")
    scrape_tokopedia(keyword)