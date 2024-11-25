from flask import Blueprint, request, jsonify
import requests
import sqlite3

# Create a Flask Blueprint
location_airport = Blueprint('location_airport', __name__)

# Database search function for airports
def search_airport_by_city(city_name):
    conn = sqlite3.connect('app/airport_codes.db')
    conn.text_factory = lambda x: x.decode('utf-8')  # Ensure UTF-8 decoding
    # conn.text_factory = str  # Handle Unicode characters
    cursor = conn.cursor()

    # Query the database for airports in the city
    cursor.execute('''
        SELECT ident, iata_code, name, municipality, iso_country
        FROM airports
        WHERE municipality LIKE ?
    ''', ('%' + city_name + '%',))

    results = cursor.fetchall()
    conn.close()

    if results:
        # Format the response for matching airports
        airports = [
            {
                "ICAO Code": ident,
                "IATA Code": iata_code,
                "Airport Name": name,
                "City": municipality,
                "Country": iso_country
            }
            for ident, iata_code, name, municipality, iso_country in results
        ]
        return airports
    else:
        return []  # No airports found

# Unified endpoint
@location_airport.route('/get-location-airports', methods=['GET'])
def get_location_airports():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # Step 1: Get latitude and longitude using Nominatim
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "FlaskAppLocationService/1.0 (almashhourhussam@gmail.com)"
    }

    try:
        response = requests.get(nominatim_url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data:
            return jsonify({"error": "No location found for the given query"}), 404

        location_result = data[0]
        latitude = location_result.get("lat")
        longitude = location_result.get("lon")
        display_name = location_result.get("display_name")

        # Step 2: Find airports in the city
        airports = search_airport_by_city(query)
        response = jsonify({
            "query": query,
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "display_name": display_name,
                "bounding_box": location_result.get("boundingbox")
            },
            "airports": airports
        })

        # Set response encoding to UTF-8
        response.headers["Content-Type"] = "application/json; charset=utf-8"

        # Return the response, ensuring special characters display correctly
        return response, 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to Nominatim API", "details": str(e)}), 500
