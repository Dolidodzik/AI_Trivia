from dotenv import load_dotenv
import os
import requests
import json
import random

load_dotenv()
api_key = os.getenv("UNSPLASH_KEY")

def get_random_image_from_country(country):
    base_url = "https://api.unsplash.com/photos/random"

    params = {
        "client_id": api_key,
        "query": country,
    }
    response = requests.get(base_url, params=params)

    remaining = response.headers.get("X-Ratelimit-Remaining")
    print("Remaining images requests: "+str(remaining))

    if response.status_code == 200:
        data = response.json()
        
        #print(data)
        print("")
        print(data['location'])
        print("")
        print("COUNTRY_LOCATION: "+data['location']['country'])

        image_url = data["urls"]["regular"]
        print(f"Random image from {country}: {image_url}")
    else:
        print(f"Error: Unable to fetch image. Status code: {response.status_code}")

#get_random_image_from_country('Slovenia')
