import operator
import functools


def product(iterable):
    """Returns the product of an iterable"""
    return functools.reduce(operator.mul, iterable)


def nslice(seq, n, truncate=False):
    """Yield slices of seq, n elements at a time"""
    assert n > 0
    while len(seq) >= n:
        yield seq[:n]
        seq = seq[n:]
    if len(seq) and not truncate:
        yield seq
