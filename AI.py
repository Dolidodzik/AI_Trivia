country_name = "Korea"

paragraphs = '''
Korean art has been highly influenced by Buddhism and Confucianism, which can be seen in the many traditional paintings, sculptures, ceramics and the performing arts. Korean pottery and porcelain, such as Joseons baekja and buncheong, and Goryeos celadon are well known throughout the world. The Korean tea ceremony, pansori, talchum, and buchaechum are also notable Korean performing arts.\nPost-war modern Korean art started to flourish in the 1960s and 1970s, when South Korean artists took interest in geometrical shapes and intangible subjects. Establishing a harmony between man and nature was also a favorite of this time. Because of social instability, social issues appeared as main subjects in the 1980s. Art was influenced by various international events and exhibits in Korea, which brought more diversity. The Olympic Sculpture Garden in 1988, the transposition of the 1993 edition of the Whitney Biennial to Seoul, the creation of the Gwangju Biennale and the Korean Pavilion at the Venice Biennale in 1995 were notable events., Robotics has been included in the list of main national research and development projects since 2003. In 2009, the government announced plans to build robot-themed parks in Incheon and Masan with a mix of public and private funding. In 2005, Korea Advanced Institute of Science and Technology (KAIST) developed the worlds second walking humanoid robot, HUBO. A team in the Korea Institute of Industrial Technology developed the first Korean android, EveR-1 in May 2006.\nEveR-1 has been succeeded by more complex models with improved movement and vision.Plans of creating English-teaching robot assistants to compensate for the shortage of teachers were announced in February 2010, with the robots being deployed to most preschools and kindergartens by 2013. Robotics are also incorporated in the entertainment sector; the Korean Robot Game Festival has been held every year since 2004 to promote science and robot technology., Korean cuisine, hanguk yori (한국요리; 韓國料理), or hansik (한식; 韓食), has evolved through centuries of social and political change. Ingredients and dishes vary by province. There are many significant regional dishes that have proliferated in different variations across the country in the present day. The Korean royal court cuisine once brought all of the unique regional specialties together for the royal family. Meals consumed both by the royal family and ordinary citizens have been regulated by a unique culture of etiquette.\nKorean cuisine is largely based on rice, noodles, tofu, vegetables, fish and meats. Traditional meals are noted for the number of side dishes, banchan (반찬), which accompany steam-cooked short-grain rice. Every meal is accompanied by numerous banchan. Kimchi (김치), a fermented, usually spicy vegetable dish is commonly served at every meal and is one of the best known dishes. Korean cuisine usually involves heavy seasoning with sesame oil, doenjang (된장, a type of fermented soybean paste), soy sauce, salt, garlic, ginger, and gochujang (고추장, a hot pepper paste). Other well-known dishes are bulgogi (불고기), grilled marinated beef; gimbap (김밥); and tteokbokki (떡볶이), a spicy snack consisting of rice cake seasoned with gochujang or a spicy chili paste.\nSoups are also a common part of a meal and are served as part of the main course rather than at the beginning or the end of the meal. Soups known as guk (국) are often made with meats, shellfish and vegetables. Similar to guk, tang (탕; 湯) has less water and is more often served in restaurants. Another type is jjigae (찌개), a stew that is typically heavily seasoned with chili pepper and served boiling hot.\nPopular Korean alcoholic drinks include Soju, Makgeolli and Bokbunja ju. Korea is unique among East Asian countries in its use of metal chopsticks. Metal chopsticks have been discovered in Goguryeo archaeological sites.
'''

instruction = '''
Above you can see 3 paragraphs of text describing a country. I am doing fun trivia quiz with my friends and I will need you to think of facts about this country, but be careful. Your output MUSNT contain name of the country. My friends will be guessing what country is this, based on facts you will give. Use simple language, mix up some details from 3 paragraphs above. 

Make it concise, dont use fancy language just focus on facts, but also dont make it boring. You are allowed to put 1 or 2 facts that are purely number based. You are allowed to put only 1 name of city (which can't be name of capital because that would be too easy). Rest of the facts you provide should be something interesting about culture, religions, cusine, geography, history, languages, famous people or stuff like that. This interesting stuff like that is very important.

Dont output me pointed list, just simple text that is around 60 words long will be enough. DO NOT MAKE IT OBVIOUS - dont talk about eifeel tower in case of france, or about nasizm in case of Germany for example because that would be too easy.DO NOT FORMAT YOUR OUTPUT AS POINTED OR NUMBERED LIST, MAKE IT PLAIN TEXT AROUND 60 WORDS LONG. DO IT IN SIMPLE LANGUAGE, LIKE TALKING TO 10 YEAR OLD, DO NOT USE OVER THE TOP VOCABULARY. AND ONCE AGAIN - YOUR OUTPUT MUSNT CONTAIN NAME OF THE ORIGINAL COUNTRY. Country you will be writing about is ''' + country_name + ' so you musnt use this word (or any other word that is derived from it) anywhere in your output.'

# cost calculations for api usage
'''
one query like this (3 paragraphs of wikipedia text + instruction) uses 1500 input tokens and 300 output tokens, or less

for mixtral:

1M input/output tokens price = 0.27$ / 1M requests (output and input tokens cost the same)

1500 + 300 = 1800 tokens per request
it will take ~550 requests like these to get to 1M tokens
1M = 0.27$
550 requests = 0.27$
'''

prompt = paragraphs + instruction 

import os
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()

# Access the environment variable by its key
deepinfra_key = os.getenv("DEEPINFRA_KEY")

# Check if the variable is set
if deepinfra_key is not None:
    print("KEY WAS READ SUCCESSFULY")
else:
    print("DEEPINFRA_KEY is not set in the .env file CANNOT CONTINUTE")
    exit()




client = OpenAI(
        api_key=deepinfra_key,
        base_url="https://api.deepinfra.com/v1/openai")

stream = False

MODEL_DI = "mistralai/Mixtral-8x7B-Instruct-v0.1"
chat_completion = client.chat.completions.create(model=MODEL_DI,
    messages=[{"role": "user", "content": prompt}],
    stream=stream,
    max_tokens=250)

print(chat_completion.choices[0].message.content)