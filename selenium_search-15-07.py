from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to perform Google search and scrape results
def google_search(query):
    # Set up the WebDriver (ensure ChromeDriver path is correct)
    service = Service('C:\\Users\\www.abcom.in\\Downloads\\python\\driver\\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        # Open Google
        driver.get("https://www.google.com")
        time.sleep(5)
        driver.maximize_window()

        # Find the search box, enter the query, and hit Enter
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        element_to_click = driver.find_element(By.XPATH, "//div[@class='S8ee5 CwbYXd wHYlTd']")
        time.sleep(5)
        driver.execute_script("window.scrollBy(0,100);", element_to_click.click())
        time.sleep(5)

        results = []

        while True:
            # Get the HTML of the page
            html = driver.page_source
            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Re-locate elements inside the loop to avoid stale references
            result_elements = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']")

            for i in range(len(result_elements)):
                retry = 0
                while retry < 3:
                    try:
                        # Re-locate the element
                        result_elements = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']")
                        result = result_elements[i]

                        # Click on each result to open the modal
                        result.click()
                        time.sleep(5)  # Wait for the modal to load

                        # Get the HTML of the modal
                        html_modal = driver.page_source
                        soup_modal = BeautifulSoup(html_modal, 'html.parser')

                        # Extract data from the modal
                        name_element = soup_modal.find('h2', class_='qrShPb')
                        name = name_element.get_text(strip=True) if name_element else 'N/A'

                        address_span = soup_modal.find('div', {'data-attrid': 'kc:/location/location:address'})
                        address = address_span.find('span', class_='LrzXr').get_text(strip=True) if address_span else 'N/A'

                        phone_span = soup_modal.find('div', {'data-attrid': 'kc:/local:alt phone'})
                        phone = phone_span.find('span', class_='LrzXr').get_text(strip=True) if phone_span else 'N/A'

                        website_anchor = soup_modal.find('a', href=True, string="Website")
                        website = website_anchor['href'] if website_anchor else 'N/A'

                        results.append({
                            'Name': name,
                            'Address': address,
                            'Phone': phone,
                            'Website': website
                        })

                        break  # Exit the retry loop on success

                    except Exception as e:
                        retry += 1
                        if retry >= 3:
                            print(f"Error interacting with result after 3 retries: {e}")
                            continue  # Continue with the next result

            try:
                next_page = driver.find_element(By.ID, 'pnnext')
                next_page.click()
                time.sleep(5)
            except:
                print("No more pages available.")
                break

        # Create a DataFrame from the results
        df = pd.DataFrame(results)
        current_time = time.strftime("%Y%m%d%H%M%S")
        # Save the DataFrame to an Excel file
        excel_file = f'{query.replace(" ", "_")}_search_results_{current_time}.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"Data successfully scraped and saved to {excel_file}")

    finally:
        driver.quit()

# Main function to take input from the user
def main():
    query = "real estate agencies in mumbai"
    google_search(query)

if __name__ == '__main__':
    main()
