#!/usr/bin/python3
from gmpy2 import powmod


def primitive_roots(m):
    """Yields the primitive roots of `m`"""
    for a in range(1, m):
        if set(powmod(a, p, m) for p in range(1, m)) == set(range(1, m)):
            yield a


if __name__ == '__main__':
    print(list(primitive_roots(11)))
