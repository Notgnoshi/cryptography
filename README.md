# Cryptography

Coursework for CSC 512, Cryptography.

* `crypto/`

    A Python (version 3) module implementing various classical ciphers, number theory/linear algebra functions, etc.

    Dependencies:
    - `gmpy2`
    - `numpy`
    - `concurrencytest` for running unittests in parallel. `runtests.py` will run tests in serial if the `concurrencytest` module is not installed
    - Tentatively `sympy`.
    - Use `sudo -H pip install gmpy2 numpy sympy concurrencytest` to install
        * `gmpy2` requires: `sudo apt install libgmp3-dev libmpc-dev libmpfr-dev`

    Example usage may be found in the course homework and in the unit tests. Run `pydoc3 -b` and navigate to `crypto` link to view the crypto library documentation.

* `homework/`

    Class homework.

* `tests/`

    Unit tests for the `crypto` library. Run with `python3 tests/runtests.py`. Some tests will be skipped if not using Python 3.6+

---

## Portfolio
* Library: `crypto/`
* Library unit tests: `tests/`
* Library examples: `examples/`

---

## TODO
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
* Convert all ciphers to take in bytes.
* DES
    - Pass in bytes, get bytes out
    - Unit test the example in the project assignment
* Differential Cryptanalysis for three rounds
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
* Remove underscores from methods that should be private to allow serving documentation with `pydoc3`
* GF(2^8) things...
