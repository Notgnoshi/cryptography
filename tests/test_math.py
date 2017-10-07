from crypto.math import *
from crypto.utilities import nslice
import math
import numpy as np
import random
import unittest


class MathTest(unittest.TestCase):
    def test_modular_matrix_inverse_1(self):
        m = np.matrix([[7, 14], [20, 19]], dtype=int)
        m_inv = np.matrix([[5, 10], [18, 21]], dtype=int)
        self.assertSequenceEqual(modular_matrix_inverse(m, 26).tolist(), m_inv.tolist())

    def test_modular_matrix_inverse_2(self):
        m = np.matrix([[1, 1, 1], [1, 2, 3], [1, 4, 9]])
        m_inv = np.matrix([[3, 3, 6], [8, 4, 10], [1, 4, 6]])
        self.assertSequenceEqual(modular_matrix_inverse(m, 11).tolist(), m_inv.tolist())

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

    def test_extended_gcd(self):
        a, b = 297, 140
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(g, a * x + b * y)

        a, b = 270, 192
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(g, a * x + b * y)

        a, b = random.randint(100000, 100000000), random.randint(100000, 100000000)
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(g, a * x + b * y)

    def test_continued_fraction_coeffs(self):
        decimal = math.sqrt(5)
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(4))]
        self.assertSequenceEqual(values, [2, 4, 4, 4])

        decimal = math.pi
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(7))]
        self.assertSequenceEqual(values, [3, 7, 15, 1, 292, 1, 1])

        decimal = math.sqrt(13)
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(6))]
        self.assertSequenceEqual(values, [3, 1, 1, 1, 1, 6])

        decimal = math.sqrt(12)
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(5))]
        self.assertSequenceEqual(values, [3, 2, 6, 2, 6])

        decimal = math.sqrt(7)
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(5))]
        self.assertSequenceEqual(values, [2, 1, 1, 1, 4])

        decimal = 3.764705882
        a_ks = fraction_coeffs(decimal)
        values = [a for a, _ in zip(a_ks, range(5))]
        # The textbook has 9803921 as the last value. I suspect this difference is due
        # to the book using more decimal places than they show in the text.
        self.assertSequenceEqual(values, [3, 1, 3, 4, 9803917])

    def test_continued_fraction_values(self):
        decimal = math.sqrt(5)
        C_ks = fraction_values(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(2, 1), (9, 4), (38, 17), (161, 72), (682, 305)])

        decimal = math.pi
        C_ks = fraction_values(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(3, 1), (22, 7), (333, 106), (355, 113), (103993, 33102)])

        decimal = math.sqrt(12)
        C_ks = fraction_values(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(3, 1), (7, 2), (45, 13), (97, 28), (627, 181)])

    def test_approximate_decimal(self):
        p, q = approximate_decimal(math.pi, 1e-2)
        self.assertEqual((p, q), (22, 7))

        p, q = approximate_decimal(math.pi, 1e-3)
        self.assertEqual((p, q), (333, 106))

        p, q = approximate_decimal(math.pi, 1e-18)
        self.assertEqual((p, q), (245850922, 78256779))


class SymbolFrequencyTest(unittest.TestCase):
    def test_counts(self):
        symbols = 'aaaabbbb'
        expected = {'a': 4, 'b': 4}
        actual = SymbolFrequencies(symbols)
        self.assertEqual(actual, expected)

    def test_proportions(self):
        symbols = 'aaaabbbb'
        expected = {'a': 1 / 2, 'b': 1 / 2}
        actual = SymbolFrequencies(symbols).proportions
        self.assertEqual(actual, expected)
