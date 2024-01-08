def askAI(input):
    client = OpenAI(
        api_key=deepinfra_key,
        base_url="https://api.deepinfra.com/v1/openai"
    )
    MODEL_DI = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    chat_completion = client.chat.completions.create(model=MODEL_DI,
        messages=[{"role": "user", "content": input}],
        stream=False,
        max_tokens=200)

    return chat_completion.choices[0].message.content

def sectionsToFacts(sections, country_name):

    base_instruction = '''
    I need you to think of facts about this country. Your output MUSNT contain name of the country. My friends will be guessing what country is this, based on facts you will give. Use simple language, mix up some details from 3 paragraphs above. 

    DO NOT, YOU MUSNT DO THESE THINGS:
    output messy, hard to understand text
    use sophisticated words
    use names of cities, countries or languages
    output more than 100 words
    make this too obvious
    do not talk about general or obvious stuff

    DO, YOU HAVE TO DO THESE THINGS:
    output list of 3 simple facts, each point should start with "#" and be just one simple short sentence
    Each fact has to be standalone and not rely on other facts
    talk like you are teacher talking to 10 years old, very simple and straightforward language
    output facts about culture, religions, cusine, geography, history, architecture, languages, famous people, how life is here, how things look
    output around 50-60 words
    include information specific for this country, specific for paragraphs provided above
    focus on interesting and fun facts

    YOUR OUTPUT ABSOLUTELY MUSNT CONTAIN NAME OF ANY COUNTRY OR LANGUAGE!!!
    GO OUTPUT 3 FACTS, NO MORE NO LESS
    '''

    filtering_instruction = '''
    Remove EVERY SINGLE name of country, language and city if there are any. Your output ABSOLUETELY MUSNT contain any name of country, language or city. Replace every such a thing with "this country" or "the countries' language" etc, you have to keep the same meaning, but get rid of names of countries, languages and cities. 

    Besides that, change as little as possible. Make list of points each point ABSOLUETLY has to start with "#".
    '''

    unfiltered_facts = askAI(sections + base_instruction)
    
    #print("\n\n ======== \n\n")
    #print(unfiltered_facts)
    #print("\n\n ======== \n\n")

    filtered_facts = askAI(unfiltered_facts + filtering_instruction)
    filtered_facts_list = [fact.strip() for fact in filtered_facts.split("#") if fact.strip()]

    return filtered_facts_list
