# Cryptography

Coursework for CSC 512, Cryptography.

* `crypto/`

    A Python (version 3) module implementing various classical ciphers, number theory/linear algebra functions, etc.

    Dependencies:
    - `gmpy2`
    - `numpy`
    - Tentatively `sympy`.
    - Use `sudo -H pip install gmpy2 numpy sympy` to install
        * `gmpy2` requires: `sudo apt install libgmp3-dev libmpc-dev libmpfr-dev`

    Example usage may be found in the course homework and in the unit tests.

* `homework/`

    Class homework.

* `tests/`

    Unit tests for the `crypto` library. Run with `python3 tests/runtests.py`.

---

## Portfolio
* Library: `crypto/`
* Library unit tests: `tests/`
* Library examples: `examples/`

---

## TODO
* Make lower/upper case consistent
* Allow for more than just `a-z` input?
* Refactor Hill cipher to be less fragile
* Classical Cipher Attacks
* Portfolio writeup
    - Documentation
    - Algorithm explanation
    - Use `pydoc3` to generate the docstrings in HTML
    - Add code examples to class and module level docstrings
    - add more verbose docstrings
    - Think about using Sphinx to generate documentation
* GCD, extended GCD
* modinverse
* Continued fractions
* Primitive roots (verification and finding)
* Convert all ciphers to take in bytes.
* DES
    - Pass in bytes, get bytes out
    - Unit test the example in the project assignment
* Differential Cryptanalysis for three rounds
* Change ToyDesCipher to four rounds
* Create script to encrypt file with cipher determined by commandline arguments
* Affine and Vigenere attacks
* One time pad (LsfrCipher?)
* sqrt(a, n)
* random_prime(bit_length)
* number factoring with three methods
* RSA (BigInt)
* Quadratic Sieve factoring
* Sieve of Sundaram
* Wheel Factorization
* Solovay–Strassen primality test
* Remove underscores from methods that should be private to allow serving documentation with `pydoc3`
