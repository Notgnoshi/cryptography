import string
from random import choice

ALPHABET = string.ascii_letters + string.digits


def gen_alnum(n):
    '''Generates an alphanumeric password of length n'''
    return ''.join(choice(ALPHABET) for i in range(n))


def gen_phrase(n):
    '''Generates an n word passphrase a la XKCD'''
    with open('/usr/share/dict/words') as f:
        words = [word.strip() for word in f]
        return ' '.join(choice(words) for i in range(n))
