"""
Unit tests for crypto library.

Each submodule loads its own doctests to verify the correctness of docstrings by defining
a load_tests(...) function in the submodule __init__.py file. The load_tests(...) function
loads doctests from the docstrings within the classes and functions defined in the submodule
as well as the submodule docstring itself.
"""


def run_once(f):
    """
        A decorator to ensure load_tests() is ran only once. Otherwise the test discovery will
        discover the load_tests() functions more than once and add the tests to the test suite.
    """
    def pass_through(loader, tests, ignore):
        """Pass through the TestSuite without adding test cases"""
        return tests

    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
        else:
            return pass_through(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def runtests():
    """
        Run the crypto library's unit tests

        Example:

        >>> from crypto.tests import runtests
        >>> runtests()
        ...
    """
    import doctest
    import unittest
    loader = unittest.TestLoader()
    # Discover all tests in the current directory that are prefixed with `test`. Also discovers
    # the doctests loaded by defining a load_tests(...) function in each submodule's __init__.py
    tests = loader.discover('.', pattern='test*.py')
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
    # Prevent calling sys.exit() just in case the user is running the tests from an interpreter.
    unittest.main(exit=False)
