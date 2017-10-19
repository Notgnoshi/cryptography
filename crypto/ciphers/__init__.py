"""
Cipher submodule of crypto. Defines several common ciphers.

Examples:

"""
from crypto.tests import run_once

from .toy_des import *
from .des import *


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.ciphers'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(toy_des))
    tests.addTests(doctest.DocTestSuite(des))
    return tests
