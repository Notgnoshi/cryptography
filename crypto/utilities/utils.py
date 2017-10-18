from collections import deque
import itertools
import functools
import operator
import string

# Lookup tables for letters and numbers
LETTER_TABLE = dict(zip(string.ascii_lowercase, range(0, 26)))
NUMBER_TABLE = dict(zip(range(0, 26), string.ascii_lowercase))


def product(iterable):
    """
        Returns the product of an iterable

        :param iterable: The iterable to take the product of
    """
    return functools.reduce(operator.mul, iterable)


def nslice(iterable, n, fill_value=None):
    """
        Yield n-tuple slices of iterable, using fill_value once iterable has
        been exhausted.
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fill_value)


def int_mapping(character):
    """Maps a given character (a-z) to an integer (0-25)"""
    return LETTER_TABLE[character.lower()]


def char_mapping(integer):
    """Maps a given integer (0-25) to a character (a-z)"""
    return NUMBER_TABLE[integer]


def wrap_around(l, n):
    """Returns a wrapped-around version of list `l` starting at index `n`"""
    queue = deque(l)
    queue.rotate(n)
    return list(queue)
