import gmpy2 as mp
import itertools


class BlumBlumShub(object):
    """Implements Blum-Blum-Shub random number sequence generators"""

    @classmethod
    def bbs(cls, p, q, x0):
        """An infinite Blum-Blum-Shub random number sequence generator"""
        n = mp.mul(p, q)
        for i in itertools.count():
            x1 = mp.powmod(x0, 2, n)
            x0 = x1
            yield x1

    @classmethod
    def bbsn(cls, p, q, x0, n):
        """A finite Blum-Blum-Shub random number sequence generator"""
        return itertools.islice(cls.bbs(p, q, x0), n)
