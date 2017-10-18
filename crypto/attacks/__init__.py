"""
Attacks submodule of crypto. Implements several attack methods of various ciphers.

Examples:

"""

from .affine import AffineAttack
from .vigenere import VigenereAttack

from crypto.tests import run_once


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.attacks'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(affine))
    tests.addTests(doctest.DocTestSuite(vigenere))
    return tests
