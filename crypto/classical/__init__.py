"""
Classical cipher submodule of crypto. Defines several classical ciphers.

* affine: Implements a classical Affine Cipher
* hill: Implements a classical Hill Block Cipher
* lfsr: Implements a Linear Feedback Shift Register Cipher
* vigenere: Implements a Vigenere Cipher
"""
from crypto.tests import run_once

from .affine import AffineCipher
from .hill import HillCipher
from .lfsr import LfsrCipher
from .vigenere import VigenereCipher


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.classical'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.classical.affine'))
    tests.addTests(doctest.DocTestSuite('crypto.classical.hill'))
    tests.addTests(doctest.DocTestSuite('crypto.classical.lfsr'))
    tests.addTests(doctest.DocTestSuite('crypto.classical.vigenere'))
    return tests
