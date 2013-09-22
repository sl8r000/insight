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

STACK_OVERFLOW_WORDS = set(''''the i to a is and in it of this my at that have for with but on am can code 
                            be not im so if how an as like when or do using from any would what me you want all 
                            there are some get method use one file then which here just help trying need work will 
                            problem ive know by does its now error thanks user function no each following way page
                            data time where has working into after dont see other first something works out tried
                            create however also could app new only up was same files them find should they doesnt
                            example make add why change two class run table set about below line issue question
                            object value try having cant please list right query application wrong anyone call fine
                            access looks show been because doing we view getting input server through image return
                            think than possible called able thank go sure seems program edit array second project 
                            found these id string used still created message button between more someone good 
                            database text output variable number script well point numbers device both even 
                            display values date looking'''.split())




def strip_tags(text):
    html = PyQuery(text)
    return html.remove('code').remove('a').text()


def simplify(text):
    text = unicode(text)

    # Need to worry about hyphens now.
    nice_character_text = regex.sub(ur"(\p{P}|\p{S}|\p{N})+", "", text)
    nice_character_text = nice_character_text.lower()
    return ' '.join(nice_character_text.split())


def pull_stop_words(text, stop_words=None):
    if stop_words is None:
        stop_words = DEFAULT_STOP_WORDS

    text_words = set(text.split())
    return list(text_words - stop_words)
