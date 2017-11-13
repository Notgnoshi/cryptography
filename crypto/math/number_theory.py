"""
Various number theory functions useful for cryptography.
"""
import math
import numpy
import gmpy2
# from sympy import Matrix


def modular_matrix_inverse(matrix, modulus):
    """Computes the modular inverse of an integer matrix."""

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


def sqrt_mod(a, n):
    """
        Computes the square root of `a` mod `n`

        Example:
    """
    raise NotImplementedError


def gcd(a, b):
    """
        Implements the Euclidea Algorithm to find the GCD of `a` and `b`.

        Example:
    """
    raise NotImplementedError


def xgcd(a, b):
    """
        Uses the Extended Euclidean Algorithm to return a triple (g, x, y) such that
        ax + by = g = gcd(a, b)

        Example:
    """
    prevx, x = 1, 0
    prevy, y = 0, 1

    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b

    return a, prevx, prevy


def primitive_roots(p):
    """
        Yields the primitive roots of `p`

        Example:
    """
    raise NotImplementedError


def is_primitive_root(a, p):
    """
        Determine if `a` is a primitive root mod `p`

        Example:
    """
    raise NotImplementedError


def wheel_factorization():
    """
        Implements Wheel Factorization to yield primes

        Example:
    """
    raise NotImplementedError


def sundaram_sieve():
    """
        Implements the Sieve of Sundaram to yield primes

        Example:
    """
    raise NotImplementedError


def eratosthenes_sieve():
    """
        Implements the Sieve of Eratosthenes to yield primes

        Example:
    """
    raise NotImplementedError
