import string
from random import choice
# Use the following more secure library for Python 3.6
# from secrets import choice

ALPHABET = string.ascii_letters + string.digits


class Passwords(object):
    """Utility class for generating secure passwords"""

    @classmethod
    def gen_alnum(cls, n):
        '''Generates an alphanumeric password of length n'''
        return ''.join(choice(ALPHABET) for i in range(n))

    @classmethod
    def gen_phrase(cls, n):
        '''Generates an n word passphrase a la XKCD'''
        with open('/usr/share/dict/words') as f:
            words = [word.strip() for word in f]
            return ' '.join(choice(words) for i in range(n))
