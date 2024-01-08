import wikipedia


def get_text_sections_from_article(article_name):

    print("Getting stuff from wikipedia about "+article_name+"...")
    p = wikipedia.page(article_name)

    print(p.images)
    print(p.url)
    print("Done.")
    print("Parsing sections...")

    separator = "==="
    sections = []
    for section in p.content.split(separator):
        stripped_section = section.strip()
        # getting rid of == See also == and everything below
        if("== See also ==" in stripped_section):
            break
        if stripped_section and len(stripped_section) > 50: # ignoring titles or very short sections
            sections.append(stripped_section)
    
    print("Sections parsed, returning correct wikipedia data.")
    return sections