"""
Utility submodule of crypto. Defines useful utilities.

Examples:

"""

from crypto.tests import run_once

from .bitwise import *
from .utilities import *
from .delegates import *


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.utilities'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(bitwise))
    tests.addTests(doctest.DocTestSuite(utilities))
    # tests.addTests(doctest.DocTestSuite(delegates))
    return tests
