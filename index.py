import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to perform a search and scrape results
def search_and_scrape(query):
    # Construct the search URL
    search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"

    # Send a request to fetch the HTML content
    response = requests.get(search_url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define lists to store the data
    titles = []
    snippets = []
    links = []

    # Scrape the search results
    results = soup.find_all('li', class_='b_algo')
    for result in results:
        title_element = result.find('h2')
        snippet_element = result.find('p')
        link_element = result.find('a')

        if title_element and snippet_element and link_element:
            titles.append(title_element.get_text())
            snippets.append(snippet_element.get_text())
            links.append(link_element['href'])

    # Create a DataFrame using the scraped data
    data = {
        'Title': titles,
        'Snippet': snippets,
        'Link': links
    }
    # print(data)
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
