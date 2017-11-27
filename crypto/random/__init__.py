"""
Random submodule of crypto. Defines various functions useful for generating random numbers and
text.

* blum_blum_shub: Implements a Blum-Blum-Shub random number generator
* LFSR: Implements a Linear Feedback Shift Register
* passwords: Defines several password generators
"""
from crypto.tests import run_once

from .blum_blum_shub import bbs, bbsn
from .passwords import generate_alnum, generate_alpha, generate_phrase
from .LFSR import LinearFeedbackShiftRegister
from .primes import random_prime


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.random'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.random.blum_blum_shub'))
    tests.addTests(doctest.DocTestSuite('crypto.random.passwords'))
    tests.addTests(doctest.DocTestSuite('crypto.random.LFSR'))
    tests.addTests(doctest.DocTestSuite('crypto.random.primes'))
    return tests
