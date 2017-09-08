#!/usr/bin/python3
import sys
sys.path.append('../')
from crypto import NumberTheory
import operator
import functools


def product(iterable):
    """Returns the product of an iterable"""
    return functools.reduce(operator.mul, iterable)


def main():
    # Test whether a product of the first n primes, plus 1 is prime. Very few are...
    for i in range(1, 101):
        p = product(NumberTheory.primes(i)) + 1
        print(i, NumberTheory.is_prime(p))


if __name__ == '__main__':
    main()
