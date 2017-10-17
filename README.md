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

* `docs/`

    Library documentation. Build by running `make` in the `docs/` directory. Other targets are `make clean` and `make view` for viewing the resultant PDF.

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
* GCD, extended GCD
* modinverse
* Continued fractions
* Primitive roots
* Convert all ciphers to take in bytes.
* DES
    - Pass in bytes, get bytes out
    - Unit test the example in the project assignment
* Differential Cryptanalysis for three rounds
* Change ToyDesCipher to four rounds
