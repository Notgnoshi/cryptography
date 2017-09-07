# Cryptography

My work for CSC 512 -- Cryptography.

* `crypto/`

    A Python module implementing various classical ciphers, number theory/linear algebra functions, etc.

    Dependencies:
    - `gmpy2`
    - `numpy`
    - Tentatively `sympy`.
    - *Strong* preference for Python 3
* `homework/`

    Class homework.
* `short/`

    Short snippets that don't really belong in the `crypto` library.
* `tests/`

    Unit tests for the `crypto` library. Ran with `python3 runtests.py`. Note that the `runtests.py` script temporarily adds the `crypto` library to the system path.
