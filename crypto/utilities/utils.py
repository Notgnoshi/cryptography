import itertools
import functools
import operator


def product(iterable):
    """Returns the product of an iterable"""
    return functools.reduce(operator.mul, iterable)


def nslice(iterable, n, fill_value=None):
    """
        Yield n-tuple slices of iterable, using fill_value once iterable has
        been exhausted.
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fill_value)
