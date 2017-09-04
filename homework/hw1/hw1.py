#!/usr/bin/python3
from math import gcd


def relatively_primes(n):
    """Yields the numbers from 0 to n that are coprime with n."""
    for i in range(n):
        if gcd(i, n) == 1:
            yield i


def main():
    for n in [26, 27, 29]:
        p = list(relatively_primes(n))
        print('p ({}, {}): {}'.format(len(p), len(p) * n, p))


if __name__ == '__main__':
    main()
