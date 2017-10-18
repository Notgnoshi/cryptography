"""
Utility submodule of crypto. Defines useful utilities.

Examples:

"""

from .bitstream import *
from .utils import *
from .text_chunker import *
from .preprocessor import *
from .delegates import *


def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.utilities'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(bitstream))
    tests.addTests(doctest.DocTestSuite(utils))
    tests.addTests(doctest.DocTestSuite(text_chunker))
    tests.addTests(doctest.DocTestSuite(preprocessor))
    # tests.addTests(doctest.DocTestSuite(delegates))
    return tests
