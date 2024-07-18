import requests
import pandas as pd

def get_current_location():
    """Get the current location of the user using a geolocation API."""
    response = requests.get('https://ipinfo.io/json')
    response.raise_for_status()
    data = response.json()
    return data['loc']  # 'loc' contains 'latitude,longitude'

def get_place_details(place_id, api_key):
    endpoint = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key,
        'fields': 'name,formatted_address,international_phone_number,website,rating,opening_hours'
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json().get('result', {})

def search_places(query, location, radius, api_key):
    endpoint = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': location,
        'radius': radius,
        'key': api_key
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def google_places_search(query, api_key, radius=1000):
    location = get_current_location()
    places = search_places(query, location, radius, api_key)

    data = []
    for place in places:
        place_id = place['place_id']
        details = get_place_details(place_id, api_key)
        data.append({
            'Name': details.get('name'),
            'Address': details.get('formatted_address'),
            'Phone Number': details.get('international_phone_number'),
            'Website': details.get('website'),
            'Rating': details.get('rating'),
            'Opening Hours': ', '.join(details.get('opening_hours', {}).get('weekday_text', []))
        })

    df = pd.DataFrame(data)
    excel_file = f'{query.replace(" ", "_")}_places_search_results.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Data successfully scraped and saved to {excel_file}")

def main():
    query = input("Enter your search query: ")
    api_key = input("Enter your Google API key: ")
    google_places_search(query, api_key)

if __name__ == '__main__':
    main()
