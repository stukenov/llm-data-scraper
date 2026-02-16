try:
    import wikipediaapi
except ModuleNotFoundError:
    print("The wikipediaapi module is not installed. Please install it to use this script.")
    exit()

# Configure your user agent here
user_agent = "YourApp/1.0 (your@email.com)"
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
page_py = wiki_wiki.page('Main_Page')

def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:60] if s.text else 'No text available'))
        if s.sections:
            print_sections(s.sections, level + 1)
        else:
            print("%s: No subsections" % ("*" * (level + 2)))

print_sections(page_py.sections)
