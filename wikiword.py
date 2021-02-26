class Wikiword():

    def __init__(self, word, lang_code):
        self.word = word
        self.lang_code = lang_code
        self.lang = lang_code

    def __repr__(self):
        return f'{self.lang} {self.word}'
    