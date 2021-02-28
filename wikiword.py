import json
import re

import numpy as np
import requests

with open('lang_codes.json') as r:
    lang_codes = json.load(r)


def strip_long_vowels(word):
    return word.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')


def parse_desc(temp):
    args = temp.split('|')


class WikiWord():

    def __init__(self, word, lang_code):
        self.word = word
        self.lang_code = lang_code
        self.lang = lang_codes[self.lang_code]

    def __repr__(self):
        return f'{self.lang} {self.word}'

    def get_title(self):
        if self.lang_code.endswith('-pro'):
            return f'Reconstruction:{self.lang}/{self.word[1:]}'
        if self.lang_code == 'la':
            return strip_long_vowels(self.word)
        return self.word

    def get_entry(self):
        url = 'https://en.wiktionary.org/w/api.php?action=parse' \
            + f'&page={self.get_title()}&prop=wikitext&format=json'
        req = requests.get(url).json()
        if req.get('parse'):
            full = req['parse']['wikitext']['*']
            res = re.search(rf'=={self.lang}==.*?(?=[^=]==[^=]|\Z)',
                            full, flags=re.DOTALL)
            if res:
                return res[0]
        return ''

    def get_descendants(self):
        reg = r'{{desc\|([^|]*?\=[^|]*?[\|\}])*(?P<lang_code>.*?)\|(?P<term>.*?)[}\|]'

        return [WikiWord(desc['term'], desc['lang_code'])
                for desc in re.finditer(reg, self.get_entry())]

    def print_descendants(self, level=0):
        print('\t'*level, self)
        for desc in self.get_descendants():
            desc.print_descendants(level+1)


