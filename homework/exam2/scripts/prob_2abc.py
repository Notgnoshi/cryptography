#!/usr/bin/python3
from itertools import product
import sys
from sympy import div, Poly
sys.path.append('../../')
from crypto.math import x, coeffs2poly

polys = [x**5 + x**4 + 1, x**5 + x**3 + 1, x**5 + x**4 + x**2 + 1]
# Convert Symbolic to Poly objects explicitly
polys = [Poly(p, x, modulus=2) for p in polys]

for p in polys:
    print('Running trial division on:', p)
    # Iterate over every possible four term (third order) polynomial
    # and repeatedly attempt to divide the prime `p` by that polynomial
    for coeffs in product([0, 1], repeat=4):
        poly = coeffs2poly(coeffs)
        # Only attempt to do the division if it is not 0 or 1
        if poly != Poly(0, x, modulus=2) and poly != Poly(1, x, modulus=2):
            divisor, remainder = div(p, poly, x, domain='GF(2)')
            if remainder == Poly(0, x, modulus=2):
                print('\tFound divisors:', poly, divisor)
