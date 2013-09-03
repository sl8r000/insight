import unicodedata
from pyquery import PyQuery
import sys

DEFAULT_STOP_WORDS = set('''a able about across after all almost also am among an and any are as at
                            be because been but by can cannot could dear did do does either else ever
                            every for from get got had has have he her hers him his how however i if 
                            in into is it its just least let like likely may me might most must my 
                            neither no nor not of off often on only or other our own rather said say
                            says she should since so some than that the their them then there these 
                            they this tis to too twas us wants was we were what when where which while 
                            who whom why will with would yet you your'''.split())


def strip_tags(text):
    html = PyQuery(text)
    return html.remove('code').remove('a').text()

def simplify(text):
    text = unicode(text)

    dash_char_numbers = [45, 2012, 2013, 2014, 2015, 2053]
    convert_hyphens_to_spaces = dict((char_number, u' ') for char_number in dash_char_numbers)
    kill_symbols_punctuation_digits = dict((char_number, None) for char_number in xrange(sys.maxunicode)
                                           if unicodedata.category(unichr(char_number))[0] in ['P', 'S', 'N'])

    no_hyphens_text = text.translate(convert_hyphens_to_spaces)
    nice_character_text = no_hyphens_text.translate(kill_symbols_punctuation_digits).lower()
    return ' '.join(nice_character_text.split())

def pull_stop_words(text, stop_words=None):
    if stop_words is None:
        stop_words = DEFAULT_STOP_WORDS

    text_words = set(text.split())
    return list(text_words - stop_words)
