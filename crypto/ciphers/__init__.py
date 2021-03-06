"""
Cipher submodule of crypto. Defines several common ciphers.

* des: Implements the DES cipher
* toy_des: Implements a toy version of the DES cipher
* rsa: Implements the RSA cipher
"""
from crypto.tests import run_once

from .toy_des import ToyDesCipher
from .des import DesCipher, DesChunker
from .rsa import BaseRsaCipher, RsaCipher, RsaChunker, RsaKeyGenerator


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    # Add the doctests in this file.
    tests.addTests(doctest.DocTestSuite('crypto.ciphers'))
    # Add class level doctests.
    tests.addTests(doctest.DocTestSuite('crypto.ciphers.toy_des'))
    tests.addTests(doctest.DocTestSuite('crypto.ciphers.des'))
    tests.addTests(doctest.DocTestSuite('crypto.ciphers.rsa'))
    return tests
