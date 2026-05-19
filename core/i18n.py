import json
import os

_translations = {}

def load_translations():
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    for lang in ['en', 'ar']:
        path = os.path.join(basedir, 'translations', f'{lang}.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                _translations[lang] = json.load(f)
        else:
            _translations[lang] = {}

def _(text, lang='en'):
    if lang not in _translations:
        return text
    return _translations[lang].get(text, text)
