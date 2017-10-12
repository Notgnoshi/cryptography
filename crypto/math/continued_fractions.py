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
    p_curr, p_prev = 1, 0
    q_curr, q_prev = 0, 1

    for ak in fraction_coeffs(decimal):
        p_next = ak * p_curr + p_prev
        q_next = ak * q_curr + q_prev
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next
        yield p_next, q_next


def approximate_decimal(decimal, tolerance):
    """
        Approximates the given decimal with a rational number to some specified tolerance.
        Returns a (num, denom) tuple.
    """
    for p, q in fraction_values(decimal):
        tol = abs(decimal - p / q)
        if tol <= tolerance:
            return p, q
