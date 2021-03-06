"""
Attacks submodule of crypto. Implements several attack methods of various ciphers.

* affine: Implements attacks on an affine cipher
* vigenere: Implements attacks on a vigenere cipher
* des: Implements a differential cryptanalysis attack on the ToyDesCipher detailed in the textbook
"""
from crypto.tests import run_once

from .affine import AffineAttack
from .vigenere import VigenereAttack
from .des import ThreeRoundDifferentialCryptanalysis


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.attacks'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.attacks.affine'))
    tests.addTests(doctest.DocTestSuite('crypto.attacks.des'))
    tests.addTests(doctest.DocTestSuite('crypto.attacks.vigenere'))
    return tests
