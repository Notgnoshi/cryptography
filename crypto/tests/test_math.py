from crypto.math import *
from crypto.utilities import nslice, product
from collections import Counter
import gmpy2
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

    def test_continued_fractions(self):
        decimal = math.sqrt(5)
        C_ks = fractions(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(2, 1), (9, 4), (38, 17), (161, 72), (682, 305)])

        decimal = math.pi
        C_ks = fractions(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(3, 1), (22, 7), (333, 106), (355, 113), (103993, 33102)])

        decimal = math.sqrt(12)
        C_ks = fractions(decimal)
        values = [a for a, _ in zip(C_ks, range(5))]
        self.assertSequenceEqual(values, [(3, 1), (7, 2), (45, 13), (97, 28), (627, 181)])

    def test_approximate_decimal(self):
        p, q = approximate_decimal(math.pi, 1e-2)
        self.assertEqual((p, q), (22, 7))

        p, q = approximate_decimal(math.pi, 1e-3)
        self.assertEqual((p, q), (333, 106))

        p, q = approximate_decimal(math.pi, 1e-18)
        self.assertEqual((p, q), (245850922, 78256779))


class PrimalityTest(unittest.TestCase):
    def test_miller_rabin_edge_cases(self):
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertFalse(is_prime(-3))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(1729))

    def test_miller_rabin_not_prime(self):
        even_not_prime = 1234987232
        self.assertFalse(is_prime(even_not_prime, method='miller-rabin'))
        odd_not_prime = 87934596237845
        self.assertFalse(is_prime(odd_not_prime, method='miller-rabin'))

    def test_miller_rabin_random_small(self):
        n = 10
        actual = random_prime(n)
        self.assertEqual(len(str(actual)), n)
        self.assertTrue(is_prime(actual))

    def test_miller_rabin_random_large(self):
        n = 200
        actual = random_prime(n)
        self.assertEqual(len(str(actual)), n)
        self.assertTrue(is_prime(actual))

    def test_miller_rabin_small_1(self):
        n = 10
        prime = random_prime(n)
        self.assertTrue(is_prime(prime))

    def test_miller_rabin_small_2(self):
        n = 200
        prime = random_prime(n)
        self.assertTrue(is_prime(prime))

    def test_miller_rabin_prime(self):
        n = 396736894567834589803
        self.assertTrue(is_prime(n, 'miller-rabin'))

        # Test several psuedo primes and carmichael numbers
        self.assertFalse(is_prime(9, 'miller-rabin'))
        self.assertFalse(is_prime(561, 'miller-rabin'))
        self.assertFalse(is_prime(1729, 'miller-rabin'))
        self.assertFalse(is_prime(2465, 'miller-rabin'))
        self.assertFalse(is_prime(52633, 'miller-rabin'))

    def test_miller_rabin_against_gmpy2(self):
        # Test that gmpy2 gives the same result against 5000 large numbers
        for i in range(50000000000, 50000005000):
            self.assertEqual(is_prime(i, 'miller-rabin'), gmpy2.is_prime(i))

    def test_fermat(self):
        n = 396736894567834589803
        self.assertTrue(is_prime(n, 'fermat'))

        # Test several psuedo primes and carmichael numbers
        self.assertFalse(is_prime(9, 'fermat'))
        self.assertFalse(is_prime(561, 'fermat'))
        self.assertFalse(is_prime(1729, 'fermat'))
        self.assertFalse(is_prime(2465, 'fermat'))
        self.assertFalse(is_prime(52633, 'fermat'))

    def test_fermat_against_gmpy2(self):
        # Test that gmpy2 gives the same result against 5000 large numbers
        for i in range(50000000000, 50000005000):
            self.assertEqual(is_prime(i, 'fermat'), gmpy2.is_prime(i))


class FactoringTest(unittest.TestCase):
    def test_factor(self):
        self.assertRaises(NotImplementedError, factor, 10, 'pollard-rho')
        self.assertRaises(NotImplementedError, factor, 10, 'pollard-p1')
        self.assertRaises(NotImplementedError, factor, 10, 'quadratic-sieve')

    def test_trial_division_factor(self):
        prime_factors = [13, 13, 19, 37, 113]
        num = product(prime_factors)
        found_factors = factor(num, 'trial-division')
        self.assertEqual(Counter(prime_factors), Counter(found_factors))

    def test_fermat_factor_1(self):
        self.assertRaises(ValueError, factor, 10, 'fermat')
        self.assertListEqual(factor(9, 'fermat'), [3, 3])
        # Note that 9 is not prime, but is still a factor.
        self.assertListEqual(factor(333, 'fermat'), [37, 9])

    def test_fermat_factor_2(self):
        prime_factors = [13, 19, 37]
        num = product(prime_factors)
        found_factors = factor(num, 'fermat')
        self.assertEqual(num, product(found_factors))
        self.assertListEqual(found_factors, [13 * 19, 37])

        # A random composite number picked from nowhere.
        num = 124987921
        found_factors = factor(num, 'fermat')
        self.assertEqual(num, product(found_factors))
        self.assertListEqual(found_factors, [690541, 181])


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
