"""
Crypto module. Defines classes and functions useful for cryptography.

* attacks: Defines several attack methods for different ciphers such as attacks on an Affine Cipher,
           Vigenere Cipher, and DES.
* ciphers: Implements several ciphers such as a simplified DES, full DES, and RSA.
* classical: Implements several classical ciphers, such as an Affine Cipher, Vigenere Cipher, and
             a Linear Feedback Shift Register Cipher.
* math: Implements different number theory, linear algebra, etc math functions
* random: Implements different random number generators and password generators, as well as
          generating random primes.
* samples: Small plaintext and ciphertext chunks to work with in several places
* tests: Defines the crypto module's unit tests. Can be imported and ran with the following:

         >>> from crypto.tests import runtests
         >>> runtests(processes=8)

         Also defines a decorator to wrap the `load_tests()` functions in each of the submodule's
         __init__.py files. This decorator ensures that each `load_tests()` is only executed once,
         and on subsequent runs just passes through the arguments unchanged.
* utilities: Implements different utilities useful for work with cryptography. Intended for
             internal use. Defines things like bitstreams, bitwise operations, bitfields, delegates,
             text preprocessing, and some iteration utilities.
"""
