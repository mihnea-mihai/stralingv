from wikiword import WikiWord

while(True):
    print('To exit press Crtl+C.')
    print('Show all descendants of a word: (example: "campus", "la")')
    print('Tests: Latin eradico, Latin audio, P-Ger gudą')
    lemma = input('Word: ')
    lang_code = input('Lang: ')

    for temp in WikiWord(lemma, lang_code).get_inherited_from():
        print(temp)
