"""
Classical cipher submodule of crypto. Defines several classical ciphers.

Examples:

>>> cipher = AffineCipher(3, 19)
>>> cipher.encrypt('affine')
'tiirgf'
"""

from .affine import AffineCipher
from .hill import HillCipher
from .lfsr import LfsrCipher
from .vigenere import VigenereCipher

from crypto.tests import run_once


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.classical'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite(affine))
    tests.addTests(doctest.DocTestSuite(hill))
    tests.addTests(doctest.DocTestSuite(lfsr))
    tests.addTests(doctest.DocTestSuite(vigenere))
    return tests
