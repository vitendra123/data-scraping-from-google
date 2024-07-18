from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to initialize the WebDriver
def initialize_driver(chrome_driver_path):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Function to perform the Google search
def perform_search(driver, query):
    driver.get("https://www.google.com")
    time.sleep(2)
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

# Function to click on the necessary element to load results
def click_initial_element(driver):
    try:
        element_to_click = driver.find_element(By.XPATH, "//div[@class='S8ee5 CwbYXd wHYlTd']")
    except NoSuchElementException:
        try:
            element_to_click = driver.find_element(By.XPATH, "//div[@class='TOQyFc p8FEIf U48fD']")
        except NoSuchElementException:
            element_to_click = None

    if element_to_click:
        element_to_click.click()
        time.sleep(2)
    else:
        print("No clickable element found.")

# Function to extract data from the modal
def extract_modal_data(driver):
    html_modal = driver.page_source
    soup_modal = BeautifulSoup(html_modal, 'html.parser')

    name_element = soup_modal.find('h2', class_='qrShPb')
    name = name_element.get_text(strip=True) if name_element else 'N/A'

    address_span = soup_modal.find('div', {'data-attrid': 'kc:/location/location:address'})
    address = address_span.find('span', class_='LrzXr').get_text(strip=True) if address_span else 'N/A'

    phone_span = soup_modal.find('div', {'data-attrid': 'kc:/local:alt phone'})
    phone = phone_span.find('span', class_='LrzXr').get_text(strip=True) if phone_span else 'N/A'

    website_anchor = soup_modal.find('a', href=True, string="Website")
    website = website_anchor['href'] if website_anchor else 'N/A'

    return {
        'Name': name,
        'Address': address,
        'Phone': phone,
        'Website': website
    }

# Function to handle pagination
def go_to_next_page(driver):
    try:
        next_page = driver.find_element(By.ID, 'pnnext')
        try:
            next_page.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", next_page)
        time.sleep(2)
        return True
    except NoSuchElementException:
        return False

# Function to save results to an Excel file
def save_results_to_excel(results, query):
    if results:
        df = pd.DataFrame(results)
        current_time = time.strftime("%Y%m%d%H%M%S")
        excel_file = f'{query.replace(" ", "_")}_search_results_{current_time}.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"Data successfully scraped and saved to {excel_file}")
    else:
        print("No data scraped.")

# Main function to perform Google search and scrape results
def google_search(query):
    driver = initialize_driver('C:\\Users\\www.abcom.in\\Downloads\\python\\driver\\chromedriver.exe')
    results = []

    try:
        perform_search(driver, query)
        click_initial_element(driver)

        while True:
            try:
                result_elements = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']") or driver.find_elements(By.XPATH, "//div[@jscontroller='xkZ6Lb']")
                for result in result_elements:
                    retry_count = 0
                    while retry_count < 3:
                        try:
                            result.click()
                            time.sleep(5)
                            result_data = extract_modal_data(driver)
                            results.append(result_data)
                            break
                        except StaleElementReferenceException:
                            print("Encountered stale element, refetching the element.")
                            result_elements = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']") or driver.find_elements(By.XPATH, "//div[@jscontroller='xkZ6Lb']")
                            retry_count += 1
                        except Exception as e:
                            print(f"Error interacting with result: {e}")
                            save_results_to_excel(results, query)  # Save results before continuing
                            break

            except StaleElementReferenceException:
                print("Encountered stale element in the result set, refetching the elements.")
                continue

            if not go_to_next_page(driver):
                print("No more pages available.")
                break

    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
    finally:
        save_results_to_excel(results, query)  # Save results at the end of the scraping process
        driver.quit()

# Main function to take input from the user
def main():
    query = "real estate agencies in mumbai"
    google_search(query)

if __name__ == '__main__':
    main()
