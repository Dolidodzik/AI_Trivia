import random

from wikipediaParser import get_text_sections_from_article
from AI import sectionsToFacts
import constants
import AI
import photos


sections = None
round_nr = 0


print("Starting the game.")

chosen_continent = "OCEANIA"
chosen_country = "Marshall Islands"

chosen_country_obj = constants.countries[chosen_continent][chosen_country]

print("Chosen country is: "+chosen_country_obj["wikipedia_id"])
sections = get_text_sections_from_article(chosen_country_obj["wikipedia_id"])


while True:
    if(len(sections) < 3):
        # if there are no sections just get the same sections but this time they will be in new random order, besides in real game it will NEVER happen so this is just for safety
        sections = get_text_sections_from_article(chosen_country_obj["wikipedia_id"])
    else:
        round_nr += 1
        print("=================")
        print("ROUND NR: "+str(round_nr))
        print("=================")

        chosen_sections = random.sample(sections, 3)
        #print("These sections were chosen: ", chosen_sections)

        sections_text = ""
        # Remove chosen sections from the original list
        for section in chosen_sections:
            sections.remove(section)
            sections_text += section
        #print("Sections that were originally selected were removed")
        
        # TO DO STUFF
        #print("\n\n Asking AI for facts about this country \n")
        print(sections_text + "\n")

        #AI_facts = sectionsToFacts(sections_text, chosen_country)
        #print(AI_facts)

        photos.get_random_image_from_country(chosen_country_obj["unsplash_id"])

        #print("\n MOCK OUTPUT OF GAME !!11! \n\n")

        print("\n \n \n === \n \n")
        user_input = input('Do you want to continue? If you do, type "yes": ')
        print(user_input)
        if(user_input == "yes"):
            pass
        else:
            print("In that case game is over.")
            exit()

        
    




