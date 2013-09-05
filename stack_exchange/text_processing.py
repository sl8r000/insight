import regex
from pyquery import PyQuery

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

    # Need to worry about hyphens now.
    nice_character_text = regex.sub(ur"(\p{P}|\p{S}|\p{N})+", "", text)

    return ' '.join(nice_character_text.split())


def pull_stop_words(text, stop_words=None):
    if stop_words is None:
        stop_words = DEFAULT_STOP_WORDS

    text_words = set(text.split())
    return list(text_words - stop_words)
