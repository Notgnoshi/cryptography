from crypto import NumberTheory
import unittest


class NumberTheoryTest(unittest.TestCase):
    def test_coprimes(self):
        expected = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        actual = list(NumberTheory.coprimes(26))
        self.assertListEqual(expected, actual)

    def test_random_prime_small(self):
        n = 10
        actual = NumberTheory.random_prime(n)
        self.assertEqual(len(str(actual)), n)

    def test_random_prime_large(self):
        n = 200
        actual = NumberTheory.random_prime(n)
        self.assertEqual(len(str(actual)), n)

    def test_is_prime_small(self):
        n = 10
        prime = NumberTheory.random_prime(n)
        self.assertTrue(NumberTheory.is_prime(prime))

    def test_is_prime_small(self):
        n = 200
        prime = NumberTheory.random_prime(n)
        self.assertTrue(NumberTheory.is_prime(prime))

    def test_is_prime(self):
        n = 396736894567834589803
        self.assertTrue(NumberTheory.is_prime(n))
