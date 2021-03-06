"""
Mathematics submodule of crypto. Defines various number theory, linear algebra, etc functions
useful to cryptography.

* continued_fractions: Defines several functions for working with continued fractions
* frequencies: Implements a symbol frequency calculator
* number_theory: Implements several useful nuber theory functions
* polynomial: Implements several GF(2^8) polynomial utility functions
"""
from crypto.tests import run_once

from .frequencies import SymbolFrequencies
from .number_theory import *
from .continued_fractions import fraction_coeffs, fractions, approximate_decimal
from .polynomial import x, gf28_mod, reduce_gf28, coeffs2poly


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.math'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.math.frequencies'))
    tests.addTests(doctest.DocTestSuite('crypto.math.number_theory'))
    tests.addTests(doctest.DocTestSuite('crypto.math.continued_fractions'))
    tests.addTests(doctest.DocTestSuite('crypto.math.polynomial'))
    return tests
