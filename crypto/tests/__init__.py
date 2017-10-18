"""
Unit tests for crypto library.

Each submodule loads its own doctests to verify the correctness of docstrings by defining
a load_tests(...) function in the submodule __init__.py file. The load_tests(...) function
loads doctests from the docstrings within the classes and functions defined in the submodule
as well as the submodule docstring itself.
"""


def runtests():
    import doctest
    import unittest
    loader = unittest.TestLoader()
    # Discover all tests in the current directory that are prefixed with `test`
    tests = loader.discover('.', pattern='test*.py')
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
    unittest.main()
