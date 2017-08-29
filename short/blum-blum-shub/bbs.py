#!/usr/bin/python3
import gmpy2 as mp
import itertools
import sys


def bbs(n, x0):
    """A Blum-Blum-Shub random number sequence generator"""
    for i in itertools.count():
        x1 = mp.powmod(x0, 2, n)
        x0 = x1
        yield x1


def main():
    p = mp.mpz(24672462467892469787)
    q = mp.mpz(396736894567834589803)
    n = mp.mul(p, q)

    x0 = mp.mpz(873245647888478349013)

    for i in itertools.islice(bbs(n, x0), 9):
        print(i)


if __name__ == '__main__':
    main()
