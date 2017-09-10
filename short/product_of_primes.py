#!/usr/bin/python3
import sys
sys.path.append('../')
from crypto.utilities import product
from crypto.math import primes, is_prime


def main():
    # Test whether a product of the first n primes, plus 1 is prime. Very few are...
    for i in range(1, 101):
        p = product(primes(i)) + 1
        print(i, is_prime(p))


if __name__ == '__main__':
    main()
