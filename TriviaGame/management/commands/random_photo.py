from django.core.management.base import BaseCommand, CommandError

from TriviaGame.models import CountryPhoto
from TriviaGame.externalAPIs.photos import get_random_photo


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("country_name", type=str)

    def handle(self, *args, **options):
        output = get_random_photo(options["country_name"])
        print("RETURN FROM get_random_photo() is: "+str(output))
