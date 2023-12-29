####################################
# GETTING PHOTOS FROM UNSPLASH API #
####################################

from datetime import datetime, timedelta
import requests
import random

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from TriviaGame.models import CountryPhoto
from TriviaGame.constants import countries




def get_random_photo(country):

    base_url = "https://api.unsplash.com/photos/random"

    params = {
        "client_id": settings.UNSPLASH_KEY,
        "query": country,
    }
    response = requests.get(base_url, params=params)

    remaining = response.headers.get("X-Ratelimit-Remaining")
    print("Remaining images requests: "+str(remaining))
    cache.set("UNSPLASH_REQUESTS_REMAINING", remaining, 3600*2) # two hours

    if response.status_code == 200:
        data = response.json()

        instance = CountryPhoto.objects.filter(unsplash_id=data["id"]).first()

        if instance is not None:
            print("object with that id already exists, skipping saving to the db part")
        else:
            instance = CountryPhoto.objects.create(
                country=country,
                url=data["urls"]["regular"],
                unsplash_id=data["id"],
                full_location_string=data['location'],
                full_URLs_list=data["urls"]
            )
            
        return instance.url
    else:
        print(f"Error: Unable to fetch image. Status code: {response.status_code}")
        print("Since API is unavailable - we're trying to access some previously stored image from this country")
        earliest_photo = CountryPhoto.objects.filter(country=country).order_by('last_time_used_in_game').first()

        if earliest_photo is not None:
            print("photo found"+earliest_photo.unsplash_id)
            earliest_photo.last_time_used_in_game = timezone.now()
            earliest_photo.times_used_in_games += 1
            earliest_photo.save()
            return earliest_photo.url
        else:
            print("No photo of this country could be found.")
            return None

def time_until_next_hour():
    current_time = datetime.now()
    next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    time_difference = next_hour - current_time
    return time_difference.total_seconds() / 60

def unused_requests_user():
    '''
    This function should be called peordically to make use that requests that would be unused, are used to store data into DB.
    Unsplash API requests allowance resets to 50 requests every new hour (so new requests are given 1:00AM, 2:00AM and so on)
    So what this function does, if it's 2 minutes before new hour, it requests unsplash api and saves data, for random countries.
    This function is secondary priority, so it will always leave at least 5 requests unused, no matter what.
    '''
    print("unused_requests_user() called")

    while True:
        if time_until_next_hour() < 59:
            print("Less than 2 minutes left until the next hour, so we can do saving.")
        else:
            print("More than 2 minutes left until the next hour, let's save requests for later.")
            return
        
        requests_remaining = cache.get("UNSPLASH_REQUESTS_REMAINING")

        if requests_remaining and int(requests_remaining) > 5:
            print("there's enough requests to continue")
        else:
            print("not enough requests to continue")
            return
        
        # at this point we made sure that there's enough requests to continue, and that it's very close before next hour comes, so we can actually do the saving
        print("doing the saving")

        unsplash_ids = []
        for region, countries_in_region in countries.items():
            for country, data in countries_in_region.items():
                if data["population"] > 1000000:
                    unsplash_ids.append(data["unsplash_id"])

        country = random.choice(unsplash_ids)
        print("Randomly chosen country in unused_requests_user() was: "+country)
        get_random_photo(country)

    