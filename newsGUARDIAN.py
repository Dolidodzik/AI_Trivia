# this idea probably doesn't make too much sense, it's hard to get news that would contribute anything to the game like this, it's better to focus on images or wikipedia stuff

from dotenv import load_dotenv
import os
import requests
import json
import random
from datetime import datetime, timedelta

load_dotenv()
api_key = os.getenv("GUARDIAN_KEY")

def get_random_news_by_country(country):
    # The Guardian API endpoint for content
    endpoint = "https://content.guardianapis.com/search"

    # Get the date from one week ago
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Set up parameters for the API request
    params = {
        'api-key': api_key,
        'q': country,
        'from-date': from_date,
        'order-by': 'newest',
        'page-size': 10,  # You can adjust this if you want more than one result
    }

    try:
        # Make the API request
        response = requests.get(endpoint, params=params)
        print(response.text)
        response.raise_for_status()  # Check for errors in the response

        # Parse the JSON response
        data = response.json()

        print(data)
    
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")

get_random_news_by_country('Poland')
