from itertools import product
from sympy import Symbol, div, Poly


x = Symbol('x')
gf28_mod = Poly(x ** 8 + x ** 4 + x ** 3 + x + 1, x, modulus=2)


def reduce_gf28(poly):
    """
        Reduces the given sympy polynomial under the GF(2**8) polynomial x**8 + x**4 + x**3 + x + 1

        Example:

        >>> # Example taken from the textbook
        >>> f = Poly(x**2 * (x**7 + x**6 + x**3 + x + 1), x, domain='GF(2)')
        >>> f
        Poly(x**9 + x**8 + x**5 + x**3 + x**2, x, modulus=2)
        >>> reduce_gf28(f)
        Poly(1, x, modulus=2)
        >>> reduce_gf28(Poly((x**2 + x + 1) * (x**8 + x**6 + x**2 + 1), x, modulus=2))
        Poly(x**7 + 1, x, modulus=2)
    """
    _, remainder = div(poly, gf28_mod, x)
    # GF(2) sets coefficients as elements of Z_2
    return remainder.as_poly(x, domain='GF(2)')


def coeffs2poly(coeffs):
    """
        Given a list of coefficients (mod 2), most significant coefficient first, return a sympy
        polynomial.

        Example:

        >>> coeffs2poly([1, 0, 1])
        Poly(x**2 + 1, x, modulus=2)
        >>> coeffs2poly([1, 0])
        Poly(x, x, modulus=2)
        >>> coeffs2poly([0, 1])
        Poly(1, x, modulus=2)
    """

    return Poly.from_list(coeffs, gens=x, domain='GF(2)')


def poly_trial_factor(poly):
    """
        Runs trial division on a sympy Poly object in order to factor it.

        Example:

        >>> p = Poly(x**5 + x**4 + 1, x, modulus=2)
        >>> poly_trial_factor(p)
        [Poly(x**3 + x + 1, x, modulus=2), Poly(x**2 + x + 1, x, modulus=2)]
        >>> p = Poly(x**5 + x**4 + x**2 + 1, x, modulus=2)
        >>> poly_trial_factor(p)
        [Poly(x**4 + x + 1, x, modulus=2), Poly(x + 1, x, modulus=2)]
    """

    divisors = []
    for coeffs in product([0, 1], repeat=poly.degree()):
        p = coeffs2poly(coeffs)
        # Only attempt to do the division if it is not 0 or 1
        if p != Poly(0, x, modulus=2) and p != Poly(1, x, modulus=2):
            divisor, remainder = div(poly, p, x, domain='GF(2)')
            if remainder == Poly(0, x, modulus=2):
                divisors.append(divisor)
    return divisors


def poly_trial_inverse(poly):
    """
        Brute force finds the multiplicative inverse of the inputted sympy Poly object
        in Z_2[x] mod x**8 + x**4 + x**3 + x + 1. Befause GF(2^8) only has 2^8 elements, a
        brute force search runs fairly quickly, so there is no need to implement something like
        fermat's method or worse.

        Example:

        >>> poly_trial_inverse(Poly(x ** 5 + 1, x, modulus=2))
        Poly(x**6 + x**5 + x**3 + x**2 + x, x, modulus=2)
        >>> poly_trial_inverse(Poly(x**2 + x + 1, x, modulus=2))
        Poly(x**7 + x**6 + x**4 + 1, x, modulus=2)
        >>> poly_trial_inverse(Poly(x**2, x, modulus=2))
        Poly(x**7 + x**6 + x**3 + x + 1, x, modulus=2)
    """

    for coeffs in product([0, 1], repeat=8):
        p = coeffs2poly(coeffs)
        result = reduce_gf28(poly * p)

        # If the multiplication gave us the multiplicative identity
        # we found the multiplicative inverse
        if result == Poly(1, x, modulus=2):
            return p
