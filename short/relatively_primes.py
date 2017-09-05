#!/usr/bin/python3
from math import gcd
import sys


def relatively_primes(n):
    """Yields the numbers from 0 to n that are coprime with n."""
    for i in range(n):
        if gcd(i, n) == 1:
            yield i


def main(nums):
    for n in nums:
        coprimes = list(relatively_primes(n))
        print('coprimes ({}, {}): {}'.format(len(coprimes), len(coprimes) * n, coprimes))


if __name__ == '__main__':
    main(map(int, sys.argv[1:]))
