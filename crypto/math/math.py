import itertools
import gmpy2
import math
import numpy
import random
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
