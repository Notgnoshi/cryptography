from crypto import NumberTheory
import unittest


class NumberTheoryTest(unittest.TestCase):
    def test_coprimes(self):
        expected = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        actual = list(NumberTheory.coprimes(26))
        self.assertListEqual(expected, actual)
