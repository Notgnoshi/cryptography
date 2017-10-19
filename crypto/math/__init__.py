"""
Mathematics submodule of crypto. Defines various number theory, linear algebra, etc functions
useful to cryptography.

Examples:

"""
from crypto.tests import run_once

from .frequencies import SymbolFrequencies
from .number_theory import *
from .continued_fractions import *


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.math'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(frequencies))
    tests.addTests(doctest.DocTestSuite(number_theory))
    tests.addTests(doctest.DocTestSuite(continued_fractions))
    return tests
