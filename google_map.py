import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_and_scrape(query):
    # Construct the search URL
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    # Send a request to fetch the HTML content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define lists to store the data
    shop_names = []
    addresses = []
    phone_numbers = []
    emails = []

    # Scrape the search results
    for result in soup.select('.VkpGBb'):
        title = result.select_one('.dbg0pd').get_text() if result.select_one('.dbg0pd') else 'N/A'
        address = result.select_one('.rllt__details.lqhpac .rllt__details').get_text() if result.select_one('.rllt__details.lqhpac .rllt__details') else 'N/A'
        snippet = result.select_one('.VkpGBb .rllt__details').get_text() if result.select_one('.VkpGBb .rllt__details') else 'N/A'

        shop_names.append(title)
        addresses.append(address)
        phone_numbers.append('N/A')  # Placeholder for phone number extraction
        emails.append('N/A')  # Placeholder for email extraction

    # Create a DataFrame using the scraped data
    data = {
        'Shop Name': shop_names,
        'Address': addresses,
        'Phone Number': phone_numbers,
        'Email': emails
    }
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    excel_file = f'{query.replace(" ", "_")}_search_results.xlsx'
    df.to_excel(excel_file, index=False)

    print(f"Data successfully scraped and saved to {excel_file}")

# Main function to take input from the user
def main():
    query = input("Enter your search query: ")
    search_and_scrape(query)

if __name__ == '__main__':
    main()
