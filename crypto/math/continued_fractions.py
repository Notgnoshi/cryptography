"""
Implements several functions for working with continued fractions.
"""

from math import floor


def fraction_coeffs(decimal):
    """
        Yields an infinite sequence of a_k's approximating the given decimal

        Example:
        >>> from math import sqrt
        >>> from itertools import islice
        >>> coeffs = fraction_coeffs(sqrt(2))
        >>> list(islice(coeffs, 4))  # Grab the first four values of the infinite sequence
        [1, 2, 2, 2]
    """
    x_k = decimal

    while True:
        a_k = floor(x_k)
        r_k = x_k - a_k
        x_k = 1 / r_k
        yield a_k


def fractions(decimal):
    """
        Yields an infinite sequence of (pk, qk) approximating the given decimal

        Example:

        >>> from math import sqrt
        >>> from itertools import islice
        >>> pq = fractions(sqrt(2))
        >>> list(islice(pq, 4))
        [(1, 1), (3, 2), (7, 5), (17, 12)]
    """
    p_curr, p_prev = 1, 0
    q_curr, q_prev = 0, 1

    for a_k in fraction_coeffs(decimal):
        p_next = a_k * p_curr + p_prev
        q_next = a_k * q_curr + q_prev
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next
        yield p_next, q_next


def approximate_decimal(decimal, tolerance):
    """
        Approximates the given decimal with a rational number to some specified tolerance.
        Returns a (num, denom) tuple.

        Example:

        >>> from math import pi
        >>> approximate_decimal(pi, 1e-5)
        (355, 113)
    """
    for num, denom in fractions(decimal):
        tol = abs(decimal - num / denom)
        if tol <= tolerance:
            return num, denom
