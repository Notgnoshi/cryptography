import string
from random import choice
# Use the following more secure library for Python 3.6
# from secrets import choice

ALPHABET = string.ascii_letters + string.digits


def generate_alpha(n):
    '''Generates an alphabetic password of length n'''
    return ''.join(choice(string.ascii_uppercase) for i in range(n))


def generate_alnum(n):
    '''Generates an alphanumeric password of length n'''
    return ''.join(choice(ALPHABET) for i in range(n))


def generate_phrase(n):
    '''Generates an n word passphrase a la XKCD'''
    with open('/usr/share/dict/words') as f:
        words = [word.strip() for word in f]
        return ' '.join(choice(words) for i in range(n))
