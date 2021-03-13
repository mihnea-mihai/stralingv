import json
import re

import numpy as np
import requests
import pprint


with open('lang_codes.json') as r:
    lang_codes = json.load(r)


def strip_long_vowels(word):
    word = word.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')
    if word.endswith('re'):
        return word[:-3]+'o'
    return word


class WikiTemplate():

    def __init__(self, arglist):
        arglist = [e.strip() for e in arglist]
        self.temp = arglist.pop(0)
        args = {}

        for e in arglist:
            if '=' in e:
                arg, val = e.split('=', maxsplit=1)
                args[arg] = val

        pos_args = [e for e in arglist if '=' not in e]

        if self.temp in ['inh', 'der', 'sl',
                         'bor', 'slbor', 'obor', 'lbor', 'ubor', 'psm']:
            args['target_lang_code'] = pos_args[0]
            args['source_lang_code'] = pos_args[1]
            try:
                args['term'] = pos_args[2]
            except:
                args['term'] = ''

        if self.temp in ['l', 'm', 'term', 'desc', 'desctree',
                         'cal', 'clq', 'calque', 'pcal',
                         'cog', 'noncog', 'ncog', 'nc']:
            args['lang_code'] = pos_args[0]
            try:
                args['term'] = pos_args[1]
            except:
                args['term'] = ''

        if re.match(r'der\d', self.temp) or re.match(r'col\d', self.temp):
            args['lang_code'] = pos_args[0]
            args['list'] = [w for w in pos_args[1:]]

        self.args = args
    
    def __repr__(self):
        return str({'name': self.temp,
        'args': self.args})


class WikiWord():

    history = set()

    def __init__(self, word, lang_code):
        self.word = word
        self.lang_code = lang_code
        self.lang = lang_codes.get(self.lang_code)
        self.entry = self.get_entry()
        self.node = f'{self.lang}\n{self.word}\n{self.meaning}'

    def __repr__(self):
        return f'{self.lang} {self.word}'

    def get_title(self):
        if not self.word:
            return ''
        if self.lang_code.endswith('-pro') or self.lang_code=='frk':
            if self.word[0] == '*':
                return f'Reconstruction:{self.lang}/{self.word[1:]}'
            else:
                return f'Reconstruction:{self.lang}/{self.word}'
        if self.lang_code == 'la':
            return strip_long_vowels(self.word)
        return self.word

    def get_entry(self):
        print(self)
        self.url = 'https://en.wiktionary.org/w/api.php?action=parse' \
            + f'&page={self.get_title()}&prop=wikitext&format=json'
        if self.url in self.history:
            self.meaning = ''
            return ''

        if ' ' in self.word:
            self.meaning = ''
            return ''        

        self.history.add(self.url)
        req = requests.get(self.url).json()
        if req.get('parse'):
            full = req['parse']['wikitext']['*']
            res = re.search(rf'=={self.lang}==.*?(?=[^=]==[^=]|\Z)',
                            full, flags=re.DOTALL)
            if res:
                meaning = re.search(r'\#.*?\[\[(?P<meaning>[ \w-]*?)\]\]', res[0])
                self.meaning = meaning['meaning'] if meaning else None
                return res[0]
        self.meaning = ''
        return ''

    def get_section(self, section):
        reg = fr'=+{section}=+.+?(?=\n=|\Z)'
        res = re.search(reg, self.entry, flags=re.DOTALL)
        return res[0] if res else ''

    def get_templates(self, section):
        reg = r'{{(?P<temp>.*?)}}'
        return [WikiTemplate(m['temp'].split('|'))
                for m in re.finditer(reg, section, flags=re.DOTALL)]

    def get_ascendants(self):
        for t in self.get_templates(self.entry):
            if t.temp in ['inh', 'bor', 'der']:
                w = WikiWord(t.args['term'], t.args['source_lang_code'])
                if w.entry:
                    yield w

    def get_descendants(self):
        lst = []
        for t in self.get_templates(self.entry):
            if t.temp == 'desc' or t.temp == 'desctree':
                w = WikiWord(t.args['term'], t.args['lang_code'])
                if w.entry:
                    lst.append(w)
            elif re.match(r'der\d', t.temp) or re.match(r'col\d', t.temp):
                for w in t.args['list']:
                    ww = WikiWord(w, t.args['lang_code'])
                    if ww.entry:
                        lst.append(ww)

        for t in self.get_templates(self.get_section('Derived terms')):
            if t.temp == 'l':
                w = WikiWord(t.args['term'], t.args['lang_code'])
                if w.entry:
                    lst.append(w)
        return lst

    def get_all_descendants(self):
        return {desc: desc.get_all_descendants() for desc in self.get_descendants()}

    def get_all_ascendants(self):
        return {asc: asc.get_all_ascendants() for asc in self.get_ascendants()}




