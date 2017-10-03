#!/usr/bin/python3
import sys
sys.path.append('../../')
from crypto.math import coprimes
from gmpy2 import powmod


def primitive_roots(m):
    """Yields the primitive roots of `m`"""
    for a in coprimes(m):
        if set(powmod(a, p, m) for p in range(1, m)) == set(coprimes(m)):
            yield a


if __name__ == '__main__':
    print(list(primitive_roots(int(sys.argv[1]))))
