import random

from wikipediaParser import get_text_sections_from_article
from AI import sectionsToFacts
import constants
import AI


sections = None
round_nr = 0


print("Starting the game.")

chosen_continent = random.choice(constants.continents)
#chosen_continent = "EUROPE"

print("Chosen continent is: "+chosen_continent)

chosen_country = random.choice(constants.country_articles[chosen_continent])
#chosen_country = "Chad (Country)"

print("Chosen country is: "+chosen_country)
sections = get_text_sections_from_article(chosen_country)


while True:
    if(len(sections) < 3):
        if(round_nr <= 0):
            print("BREAK ERROR SECTIONS TOO SHORT SOMETHING WENT WRONG")
            exit()
        else:
            print("NO MORE SECTIONS LEFT TO MAKE INTERESTING FACTS")
            break
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
        print("\n\n Asking AI for facts about this country \n")

        AI_facts = sectionsToFacts(sections_text, chosen_country)
        print(AI_facts)

        print("\n MOCK OUTPUT OF GAME !!11! \n\n")

        user_input = input('Do you want to continue? If you do, type "yes": ')
        print(user_input)
        if(user_input == "yes"):
            pass
        else:
            print("In that case game is over.")
            exit()

        
    




