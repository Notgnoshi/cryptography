"""
Utility submodule of crypto. Defines useful utilities.

Examples:

"""

from .bitstream import *
from .utils import *
from .delegates import *

from crypto.tests import run_once


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.utilities'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(bitstream))
    tests.addTests(doctest.DocTestSuite(utils))
    # tests.addTests(doctest.DocTestSuite(delegates))
    return tests
