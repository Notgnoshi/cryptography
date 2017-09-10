from crypto import Math
from crypto import NumberTheory
import numpy as np
import unittest


class MathTest(unittest.TestCase):
    def test_modular_matrix_inverse(self):
        m = np.matrix([[7, 14], [20, 19]])
        m_inv = np.matrix([[5, 10], [18, 21]], dtype=int)
        self.assertSequenceEqual(Math.modular_matrix_inverse(m, 26).tolist(), m_inv.tolist())


class NumberTheoryTest(unittest.TestCase):
    def test_infinite_prime_generator(self):
        generator = NumberTheory.primes()
        ten_primes = [next(generator) for i in range(10)]
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertListEqual(ten_primes, expected)

    def test_finite_prime_generator(self):
        ten_primes = list(NumberTheory.primes(10))
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertListEqual(ten_primes, expected)
