from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the webdriver (make sure chromedriver is in your PATH or specify the path)
driver = webdriver.Chrome()

def search_business(query):
    # Open Google Search
    driver.get("https://www.google.com/")
    
    # Find the search box and enter the query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Allow time for search results to load
    
    # Locate the section containing the business details
    business_section = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="title"]')
    
    # Extract business name
    business_name = business_section.find_element(By.TAG_NAME, 'span').text
    
    # Extract other business details
    try:
        business_address = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:address"]').text
    except:
        business_address = 'N/A'
    
    try:
        business_phone = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:phone"]').text
    except:
        business_phone = 'N/A'
    
    try:
        business_website = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:website"]').text
    except:
        business_website = 'N/A'
    
    try:
        business_rating = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:star rating"]').text
    except:
        business_rating = 'N/A'
    
    # Print the scraped data
    print(f"Business Name: {business_name}")
    print(f"Address: {business_address}")
    print(f"Phone: {business_phone}")
    print(f"Website: {business_website}")
    print(f"Rating: {business_rating}")
    
    # Close the driver
    driver.quit()

# Use the function to search for a business
search_query = "Coffee shop near me"
search_business(search_query)
