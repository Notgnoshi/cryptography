"""
Utility submodule of crypto. Defines useful utilities.

* bitwise: Defines several useful functions and classes for working with binary data in Python
* delegates: Unused as of yet, but defines classes implementing the delegate design pattern
* utilities: Miscellaneous utilities primarily dealing with iteration and working with text
"""

from crypto.tests import run_once

from .bitfield import Bitfield
from .bitwise import *
from .utilities import *
from .delegates import Delegated


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.utilities'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.utilities.bitwise'))
    tests.addTests(doctest.DocTestSuite('crypto.utilities.bitfield'))
    tests.addTests(doctest.DocTestSuite('crypto.utilities.utilities'))
    tests.addTests(doctest.DocTestSuite('crypto.utilities.delegates'))
    return tests
