from math import floor


def fraction_coeffs(decimal):
    """Yields an infinite sequence of ak's approximating the given decimal"""
    xk = decimal

    while True:
        ak = floor(xk)
        rk = xk - ak
        xk = 1 / rk
        yield ak


def fraction_values(decimal):
    """Yields an infinite sequence of (pk, qk) approximating the given decimal"""
    p_k1 = 1
    p_k2 = 0
    q_k1 = 0
    q_k2 = 1

    for ak in fraction_coeffs(decimal):
        p_k = ak * p_k1 + p_k2
        q_k = ak * q_k1 + q_k2
        p_k2, p_k1 = p_k1, p_k
        q_k2, q_k1 = q_k1, q_k
        yield p_k, q_k


def approximate_decimal(decimal, tolerance):
    """
        Approximates the given decimal with a rational number to some specified tolerance.
        Returns a (num, denom) tuple.
    """
    for p, q in fraction_values(decimal):
        tol = abs(decimal - p / q)
        if tol <= tolerance:
            return p, q
