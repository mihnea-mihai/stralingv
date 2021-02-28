from wikiword import WikiWord

while(True):
    print('To exit press Crtl+C.')
    print('Show all descendants of a word: (example: "campus", "la")')
    lemma = input('Word: ')
    lang_code = input('Lang: ')
    WikiWord(lemma, lang_code).print_descendants()