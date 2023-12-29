####################################
# GETTING PHOTOS FROM UNSPLASH API #
####################################

from django.conf import settings
import requests
from TriviaGame.models import CountryPhoto
from django.utils import timezone


def get_random_photo(country):

    base_url = "https://api.unsplash.com/photos/random"

    params = {
        "client_id": "settings.UNSPLASH_KEY",
        "query": country,
    }
    response = requests.get(base_url, params=params)

    remaining = response.headers.get("X-Ratelimit-Remaining")
    print("Remaining images requests: "+str(remaining))

    if response.status_code == 200:
        data = response.json()

        instance, created = CountryPhoto.objects.get_or_create(
            country=country,
            url=data["urls"]["regular"],
            unsplash_id=data["id"],
            full_location_string=data['location'],
            full_URLs_list=data["urls"]
        )

        if created:
            print("new instance created")
        else: 
            print("the same thing already existed in db, not saving anything")
        
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

