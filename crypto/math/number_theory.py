"""
Various number theory functions useful for cryptography.
"""

import itertools
import math
import random
import numpy
import gmpy2
# from sympy import Matrix


def modular_matrix_inverse(matrix, modulus):
    """Computes the modular inverse of an integer matrix given by the formula
       M^{-1} \pmod{n} = \det(A)^{-1} \mod{n} \cdot (\det(A) A^{-1}) \pmod{n}"""

    # If sympy import times are not an issue, the following works, and is probably more reliable
    # return Matrix(matrix).inv_mod(modulus)

    m_inv = numpy.linalg.inv(matrix)
    # Round and convert to an integer
    det = int(round(numpy.linalg.det(matrix)))
    det_inv = int(gmpy2.invert(det, modulus))
    return numpy.around(numpy.mod(det_inv * (det * m_inv), modulus))


def coprimes(num):
    """
        Yields the numbers from 1 to `num` that are coprime with `num`.

        Example:

        >>> list(coprimes(5))
        [1, 2, 3, 4]
    """
    return iter(filter(lambda x: math.gcd(x, num) == 1, range(num)))


def prime_pi(n):
    """Returns the number of primes less than n"""
    # Alternatively: return sympy.primepi(n)
    return n / math.log(n)


def random_prime(digits):
    """Generates a random large prime number with `digits` digits"""
    # TODO: There's got to be a better implementation than this...
    # Generate a random number with n digits
    num = random.randint(10**(digits - 1) + 1, 10**digits)
    # Find the next prime after the number - will *probably* have n digits.
    return gmpy2.next_prime(num)


def is_prime(x):
    """Returns True if x is probably prime, False otherwise. Runs 25 Miller-Rabin tests."""
    return gmpy2.is_prime(x, 25)


def _primes():
    """An infinite prime generator for internal use."""
    start = 1
    while True:
        # Convert from mpz() to Python int
        start = int(gmpy2.next_prime(start))
        yield start


def primes(limit=None):
    """
        A generator that yields the first `limit` primes. Defaults to infinite primes.
        Uses gmpy2.next_prime() to generate prime after prime.

        Example:

        >>> p = primes(10)
        >>> list(p)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit is None:
        return _primes()
    return itertools.islice(_primes(), limit)


def extended_gcd(a, b):
    """Uses the Extended Euclidean Algorithm to return a triple (g, x, y) such that
       ax + by = g = gcd(a, b)"""
    prevx, x = 1, 0
    prevy, y = 0, 1

    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b

    return a, prevx, prevy
