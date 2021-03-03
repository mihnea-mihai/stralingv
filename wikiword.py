import json
import re

import numpy as np
import requests

with open('lang_codes.json') as r:
    lang_codes = json.load(r)


def strip_long_vowels(word):
    return word.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')


def parse_arglist(arglist):

    args = {'temp': arglist[0]}
    
    for e in arglist:
        if '=' in e:
            arg, val = e.split('=', maxsplit=1)
            args[arg] = val

    pos_args = [e for e in arglist if '=' not in e]

    if args['temp'] in ['inh', 'der', 'bor']:
        args['target_lang_code'] = pos_args[1]
        args['source_lang_code'] = pos_args[2]
        try:
            args['term'] = pos_args[3]
        except:
            args['term'] = ''

    if args['temp'] in ['l', 'm', 'term', 'desc']:
        args['lang_code'] = pos_args[1]
        try:
            args['term'] = pos_args[2]
        except:
            args['term'] = ''

    return args


def parse_temp(temp):
    return parse_arglist(temp.split('|'))


class WikiWord():

    def __init__(self, word, lang_code):
        self.word = word
        self.lang_code = lang_code
        self.lang = lang_codes[self.lang_code]
        self.node = f'{self.lang}\n{self.word}'

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

    def get_templates_(self):
        reg = r'{{(?P<temp>.*?)}}'
        return [parse_temp(m['temp'])
                for m in re.finditer(reg, self.get_entry())]

    def get_templates(self):
        try:
            return self.templates
        except:
            self.templates = self.get_templates_()
            return self.templates

    def get_ascendants(self, asc):
        ascs = []
        for t in self.get_templates():
            if asc == None or t['temp'] == asc:
                if t['term'] not in ['-', '']:
                    ascs.append(WikiWord(t['term'], t['source_lang_code']))
        return ascs

    def get_descendants(self):
        for t in self.get_templates():
            if t['temp'] == 'desc':
                if t['term'] not in ['-', '', None]:
                    yield(WikiWord(t['term'], t['lang_code']))

    """

    def print_descendants(self, level=0):
        print('\t'*level, self)
        for desc in self.get_descendants():
            desc.print_descendants(level+1)
    """
