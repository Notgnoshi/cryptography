#!/usr/bin/python3
# import os
# import sys
import unittest


if __name__ == '__main__':
    # Add the crypto library to path, necessary if runtests.py is in tests/
    # test_dir = os.path.dirname(__file__)
    # src_dir = '../'
    # sys.path.insert(0, os.path.abspath(os.path.join(test_dir, src_dir)))

    loader = unittest.TestLoader()
    # Discover all tests in the `crypto/tests/` directory that are prefixed with `test`
    tests = loader.discover('.', pattern='test*.py')
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
    unittest.main()
