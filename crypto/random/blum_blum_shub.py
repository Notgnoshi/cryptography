import itertools


def bbs(p, q, x0):
    """
        An infinite-length Blum-Blum-Shub random number sequence generator

        Example:
        >>> p = 24672462467892469787
        >>> q = 396736894567834589803
        >>> x0 = 873245647888478349013
        >>> gen = bbs(p, q, x0)
        >>> next(gen)
        8845298710478780097089917746010122863172
    """
    n = p * q
    for _ in itertools.count():
        x1 = pow(x0, 2, n)
        x0 = x1
        yield x1


def bbsn(p, q, x0, n):
    """
        A finite Blum-Blum-Shub random number sequence generator

        Example:
        >>> p = 24672462467892469787
        >>> q = 396736894567834589803
        >>> x0 = 873245647888478349013
        >>> gen = bbsn(p, q, x0, 10)
        >>> next(gen)
        8845298710478780097089917746010122863172
    """
    return itertools.islice(bbs(p, q, x0), n)
