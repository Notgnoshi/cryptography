"""
Random submodule of crypto. Defines various functions useful for generating random numbers and
text.

* blum_blum_shub: Implements a Blum-Blum-Shub random number generator
* LFSR: Implements a Linear Feedback Shift Register
* passwords: Defines several password generators
"""
from crypto.tests import run_once

from .blum_blum_shub import *
from .passwords import *
from .LFSR import *


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
