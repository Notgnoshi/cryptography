"""
Random submodule of crypto. Defines various functions useful for generating random numbers and
text.

Examples:

"""

from .blum_blum_shub import *
from .passwords import *
from .LFSR import *

from crypto.tests import run_once


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.random'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(blum_blum_shub))
    tests.addTests(doctest.DocTestSuite(passwords))
    tests.addTests(doctest.DocTestSuite(LFSR))
    return tests
