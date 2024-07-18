import requests
import pandas as pd
import time

def get_current_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()
        data = response.json()
        loc = data['loc']
        return loc  # returns 'latitude,longitude'
    except requests.RequestException as e:
        print(f"Error getting location: {e}")
        return None

def search_and_scrape(query, api_key, location, radius=1000):
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': location,
        'radius': radius,
        'type': 'doctor',  # or 'clinic' or any other place type
        'keyword': query,
        'key': api_key
    }

    all_places = []
    while True:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()
        print(results)
        places = results.get('results', [])
        all_places.extend(places)

        # Check if there are more results available
        if 'next_page_token' in results:
            params['pagetoken'] = results['next_page_token']
            # Pause to avoid hitting API rate limits
            time.sleep(2)
        else:
            break

    # Extract the required details
    shop_names = [place.get('name', 'N/A') for place in all_places]
    addresses = [place.get('vicinity', 'N/A') for place in all_places]
    phone_numbers = ['N/A' for _ in all_places]  # Placeholder as the Places API Nearby Search doesn't return phone numbers
    emails = ['N/A' for _ in all_places]  # Placeholder as the Places API Nearby Search doesn't return emails

    # Create a DataFrame using the scraped data
    data = {
        'Shop Name': shop_names,
        'Address': addresses,
        'Phone Number': phone_numbers,
        'Email': emails
    }
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    # excel_file = f'{query.replace(" ", "_")}_search_results.xlsx'
    # df.to_excel(excel_file, index=False)

    # print(f"Data successfully scraped and saved to {excel_file}")

# Main function to take input from the user
def main():
    query = input("Enter your search query: ")
    # api_key = input("Enter your Google Places API key: ")
    api_key = 'AIzaSyC32d6RbksLRKsO8WitmcIT-gYJAr3KyqQ'
    # cx = '64407330f232c4720'
    location = get_current_location()
    if not location:
        print("Unable to get current location. Exiting.")
        return

    search_and_scrape(query, api_key, location)

if __name__ == '__main__':
    main()
