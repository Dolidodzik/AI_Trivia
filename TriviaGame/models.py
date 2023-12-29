from django.db import models

class CountryInfoCommonData(models.Model):
    country = models.CharField(max_length=100)
    times_used_in_games = models.IntegerField(default=0) 
    last_time_used_in_game = models.DateTimeField(auto_now_add=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CountryPhoto(CountryInfoCommonData):
    url = models.URLField(max_length=200)
    unsplash_id = models.CharField(max_length=20, unique=True)

    # these are technically not necessary for now, but I am storing this data just in case
    full_location_string = models.TextField()
    full_URLs_list = models.TextField()

    def __str__(self):
        return self.country + " / " + self.unsplash_id

class CountryFact(CountryInfoCommonData):
    fact = models.URLField(max_length=200)



