"""
Cipher submodule of crypto. Defines several common ciphers.

Examples:

"""

from .toy_des import *
from .des import *


def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.ciphers'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(toy_des))
    tests.addTests(doctest.DocTestSuite(des))
    return tests
