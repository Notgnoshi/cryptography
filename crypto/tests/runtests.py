#!/usr/bin/python3
import os
import sys
import unittest

if __name__ == '__main__':
    # Add the crypto library to path
    sys.path.insert(0, '../../')
    loader = unittest.TestLoader()
    # Discover tests in the current directory that are prefixed with `test`
    tests = loader.discover('.', pattern='test*.py')
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
    unittest.main()
