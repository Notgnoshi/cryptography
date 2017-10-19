"""
Misc utilities useful for large projects. Mostly related to iteration and sequences.
"""

from collections import deque
import itertools
import functools
import operator
import string

# Lookup tables for letters and numbers
LETTER_TABLE = dict(zip(string.ascii_lowercase, range(0, 26)))
NUMBER_TABLE = dict(zip(range(0, 26), string.ascii_lowercase))
ALPHABET = frozenset(string.ascii_lowercase)


def preprocess(text, use_ascii=True):
    """
        Preprocess text. Converts to lowercase and filters non-alphabetic characters.
        Defaults to defining alphabetic characters as ascii-alphabetic

        Examples:

        >>> text = 'ABC.,#'
        >>> ''.join(preprocess(text))
        'abc'
        >>> text = 'ÈÆÖÉEAEOE,.%'
        >>> ''.join(preprocess(text, use_ascii=False))
        'èæöéeaeoe'
    """
    if use_ascii:
        return filter(ALPHABET.__contains__, text.lower())
    return filter(str.isalpha, text.lower())


def product(iterable):
    """
        Returns the product of an iterable. Note the iterable does not need to be a sequence,
        i.e. it will consume generators and return a generator itself.

        Examples:

        >>> it = [1, 2, 3]
        >>> product(it)
        6

        >>> it = range(1, 5)
        >>> product(it)
        24
    """
    return functools.reduce(operator.mul, iterable)


def nslice(iterable, slice_size, fill_value=None):
    """
        Yield `slice_size`-tuple slices of `iterable`, using `fill_value` once
        iterable has been exhausted.

        Example:

        >>> it = range(0, 10)  # 0..9
        >>> slices = nslice(it, 2)
        >>> next(slices)
        (0, 1)
        >>> next(slices)
        (2, 3)
    """
    args = [iter(iterable)] * slice_size
    return itertools.zip_longest(*args, fillvalue=fill_value)


def chunker(text, chunk_size=5, fill_value=None):
    """
        Returns chunk after chunk of `text` with chunk size `chunk_size`
        and fill character `fill_value`. Equivalent to using ''.join() on
        each output of crypto.utilities.nslice.

        Example:

        >>> s = 'abcdefg'
        >>> c = chunker(s, 3, 'x')
        >>> next(c)
        'abc'
        >>> next(c)
        'def'
        >>> next(c)
        'gxx'
    """
    for chunk in nslice(text, chunk_size, fill_value=fill_value):
        yield ''.join(chunk)


def int_mapping(character):
    """
        Maps a given character (a-z) to an integer (0-25)

        Example:

        >>> int_mapping('a')
        0
        >>> int_mapping('z')
        25
    """
    return LETTER_TABLE[character.lower()]


def char_mapping(integer):
    """
        Maps a given integer (0-25) to a character (a-z)

        Example:

        >>> char_mapping(0)
        'a'
        >>> char_mapping(25)
        'z'
    """
    return NUMBER_TABLE[integer]


def wrap_around(seq, shift):
    """
        Returns a wrapped-around version of list `l` starting at index `n`

        Example:

        >>> l = [1, 2, 3, 4]
        >>> wrap_around(l, 1)  # A right rotation by one
        [4, 1, 2, 3]
        >>> wrap_around(l, -1)  # A left rotation by one
        [2, 3, 4, 1]
    """
    queue = deque(seq)
    queue.rotate(shift)
    return list(queue)
