#!/usr/bin/python3
from itertools import product
import sys
from sympy import Poly
sys.path.append('../../')
from crypto.math import x, coeffs2poly, reduce_gf28

f = Poly(x ** 5 + 1, x, modulus=2)
# Iterate over all 8 term (7th degree) polynomials
for coeffs in product([0, 1], repeat=8):
    poly = coeffs2poly(coeffs)
    result = reduce_gf28(f * poly)

    # If the multiplication gave us the multiplicative identity
    # we found the multiplicative inverse
    if result == Poly(1, x, modulus=2):
        print(poly, 'is the multiplicative inverse of', f)
