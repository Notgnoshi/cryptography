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

* `short/`

    Short snippets that don't really belong in the `crypto` library.

* `tests/`

    Unit tests for the `crypto` library. Run with `python3 tests/runtests.py`.

---

## Portfolio
* Library: `crypto/`
* Library unit tests: `tests/`
* Library examples: `examples/`
* Documentation/writeup LaTeX source: `doc/`

---

## TODO
* **Enigma simulator**
* Make lower/upper case consistent
* Allow for more than just `a-z` input
* Classical Cipher Attacks
* Portfolio writeup
    - Documentation
    - Algorithm explanation
