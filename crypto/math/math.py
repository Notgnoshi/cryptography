import itertools
import gmpy2
import math
import numpy
import random


def modular_matrix_inverse(matrix, modulus):
    """Computes the modular inverse of an integer matrix given by the formula
       M^{-1} \pmod{n} = \det(A)^{-1} \mod{n} \cdot (\det(A) A^{-1}) \pmod{n}"""

    # If sympy import times are not an issue, the following works, and is probably more reliable
    # from sympy import Matrix
    # return Matrix(matrix).inv_mod(modulus)

    # Make sure the input is a numpy integer matrix
    m = numpy.matrix(matrix, dtype=int)
    m_inv = numpy.linalg.inv(m)
    # Round and convert to an integer
    det = int(round(numpy.linalg.det(m)))
    det_inv = gmpy2.invert(det, modulus)
    return numpy.mod(det_inv * (det * m_inv), modulus).astype(int)


def coprimes(n):
    """Yields the numbers from 0 to n that are coprime with n."""
    return iter(filter(lambda x: math.gcd(x, n) == 1, range(n)))


def prime_pi(n):
    """Returns the number of primes less than n"""
    return n / math.log(n)


def random_prime(n):
    """Generates a random large prime number with n digits"""
    # Generate a random number with n digits
    num = random.randint(10**(n - 1) + 1, 10**n)
    # Find the next prime after the number - will *probably* have n digits.
    return gmpy2.next_prime(num)


def is_prime(x):
    """Returns True if x is probably prime, False otherwise. Runs 25 Miller-Rabin tests."""
    return gmpy2.is_prime(x, 25)


def _primes():
    """An infinite prime generator."""
    start = 1
    while True:
        start = gmpy2.next_prime(start)
        yield start


def primes(n=None):
    """A generator that yields the first n primes. Defaults to infinite primes."""
    if n is None:
        return _primes()
    else:
        return itertools.islice(_primes(), n)
