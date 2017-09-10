from crypto.math import *
import numpy as np
import unittest


class MathTest(unittest.TestCase):
    def test_modular_matrix_inverse(self):
        m = np.matrix([[7, 14], [20, 19]])
        m_inv = np.matrix([[5, 10], [18, 21]], dtype=int)
        self.assertSequenceEqual(modular_matrix_inverse(m, 26).tolist(), m_inv.tolist())

    def test_infinite_prime_generator(self):
        generator = primes()
        ten_primes = [next(generator) for i in range(10)]
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertListEqual(ten_primes, expected)

    def test_finite_prime_generator(self):
        ten_primes = list(primes(10))
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertListEqual(ten_primes, expected)

    def test_coprimes(self):
        expected = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        actual = list(coprimes(26))
        self.assertListEqual(expected, actual)

    def test_random_prime_small(self):
        n = 10
        actual = random_prime(n)
        self.assertEqual(len(str(actual)), n)
        self.assertTrue(is_prime(actual))

    def test_random_prime_large(self):
        n = 200
        actual = random_prime(n)
        self.assertEqual(len(str(actual)), n)
        self.assertTrue(is_prime(actual))

    def test_is_prime_small(self):
        n = 10
        prime = random_prime(n)
        self.assertTrue(is_prime(prime))

    def test_is_prime_small(self):
        n = 200
        prime = random_prime(n)
        self.assertTrue(is_prime(prime))

    def test_is_prime(self):
        n = 396736894567834589803
        self.assertTrue(is_prime(n))
