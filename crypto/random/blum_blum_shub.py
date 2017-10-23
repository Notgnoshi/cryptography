import itertools
import gmpy2 as mp


def bbs(p, q, x0):
    """An infinite Blum-Blum-Shub random number sequence generator"""
    n = mp.mul(p, q)
    for _ in itertools.count():
        x1 = mp.powmod(x0, 2, n)
        x0 = x1
        yield x1


def bbsn(p, q, x0, n):
    """A finite Blum-Blum-Shub random number sequence generator"""
    return itertools.islice(bbs(p, q, x0), n)
