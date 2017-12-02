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
