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


    # Open Google
    driver.get("https://www.google.com")
    time.sleep(5)
    driver.maximize_window()

    # Find the search box, enter the query, and hit Enter
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    #driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
    time.sleep(2)

    element_to_click = driver.find_element(By.XPATH,"//div[@class='S8ee5 CwbYXd wHYlTd']")
    time.sleep(5)
 #   driver.execute_script("arguments[0].scrollIntoView();", element_to_click)
    driver.execute_script("window.scrollBy(0,100);",element_to_click.click())

    time.sleep(5)
    #element_to_click.click()
    time.sleep(5)
    results = []
    while True:
      
        # Get the HTML of the page
        html = driver.page_source

        # You can now use BeautifulSoup to parse the HTML
        
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        # elements = driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']")

        # # Iterate over the elements and click each one
        # for element in elements:
        #     # print(f"Clicking on element: {element.text}")
        #     # time.sleep(1)  # Pause for a second to observe the click action
        #     element.click()
        #     time.sleep(5)
        #     models = driver.find_element(By.XPATH, "//div[@jsmodel='nqQQld']")
        #     # for model in models:
        #     print(f"Clicking on element: {models.text}")
        #     time.sleep(5)
        #     close = driver.find_element(By.XPATH, "//span[@class='z1asCe rzyADb']")
        #     close.click()
            # alert = driver.switch_to.alert 
            # print(f"Alert text: {alert.text}")
        for result in driver.find_elements(By.XPATH, "//div[@jscontroller='AtSb']"):
        # for result in soup.find_all('div', jscontroller="AtSb"):
            # print(result)
            result.click()
            time.sleep(5)
            # # models = driver.find_element(By.XPATH, "//div[@jsmodel='nqQQld']")
            models = soup.find_all('div', jsmodel="nqQQld")
            for div in models:
                # print(div)
            # Extract name
                name_element = div.find('h2', class_='qrShPb')
                name = name_element.get_text(strip=True) if name_element else 'N/A'
                # name = div.select_one('.qrShPb').text if result.select_one('.qrShPb') else 'N/A'

                # # Extract address
                address_span = div.find('div', {'data-attrid': 'kc:/location/location:address'})
                address = address_span.find('span', class_='LrzXr').get_text(strip=True) if address_span else 'N/A'
                # address = result.select_one('.rllt__details div:nth-child(3)').text if result.select_one('.rllt__details div:nth-child(3)') else 'N/A'
                # # Extract phone
                # phone_span = soup.find('div', {'data-attrid': 'kc:/location/location:phone'})
                # phone = phone_span.find('span', class_='LrzXr').get_text(strip=True) if phone_span else 'N/A'

                # # Extract website
                # website_anchor = soup.find('a', class_='n1obkb')
                # website = website_anchor['href'] if website_anchor else 'N/A'

                # Display extracted information
                print(f"Name: {name}")
                print(f"Address: {address}")
                # print(f"Phone: {phone}")
                # print(f"Website: {website}")
            # # print(models.text)
            # time.sleep(5)
            # name = result.select_one('.dbg0pd').text if result.select_one('.dbg0pd') else 'N/A'
            # # phone = result.select_one('.rllt__details span span').text if result.select_one('.rllt__details span span') else 'N/A'
            # phone_element = result.select_one('.rllt__details > div:nth-child(4)')
            # phone = phone_element.text.split('·')[-1].strip() if phone_element else 'N/A'
            # # print(phone)
            # # return
            # address = result.select_one('.rllt__details div:nth-child(3)').text if result.select_one('.rllt__details div:nth-child(3)') else 'N/A'
            # website_tag = result.find('a', href=True, text="Website")
            # website = website_tag['href'] if website_tag else 'N/A'
      
            # results.append({
            #     'Name': name,
            #     'Address': address,
            #     'Phone': phone,
            #     'Website': website
            # })
        # for result in results:
        #     print(result)

        # try:
        #     next_page = driver.find_element(By.ID, 'pnnext')
        #     next_page.click()
        #     time.sleep(5)
        # except:
        #     print("No more pages available.")
        #     break
        break
       
        #     # Create a DataFrame from the results
    df = pd.DataFrame(results)
    current_time = time.strftime("%Y%m%d%H%M%S")
    # # Save the DataFrame to an Excel file
    excel_file = f'{query.replace(" ", "_")}_search_results_{current_time}.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Data successfully scraped and saved to {excel_file}")
  
#        time.sleep(10)
 #       driver.quit()

# Main function to take input from the user
def main():
    # query = input("Enter your search query: ")
    query = "doctor near me"
    google_search(query)

if __name__ == '__main__':
    main()
