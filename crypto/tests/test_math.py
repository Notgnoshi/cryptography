from crypto.math import *
from crypto.utilities import nslice, product
from crypto.random import random_prime
from collections import Counter
import gmpy2
import math
import numpy as np
import random
import sys
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
        g, x, y = xgcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(g, a * x + b * y)

        a, b = 270, 192
        g, x, y = xgcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(g, a * x + b * y)

        a, b = random.randint(100000, 100000000), random.randint(100000, 100000000)
        g, x, y = xgcd(a, b)
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

    def test_legendre_properties(self):
        p = 7
        a = 4
        # 11 = 4 (mod 7)
        b = 11
        self.assertEqual(legendre(a, p), legendre(b, p))

        p = random_prime(100)
        a = random.randint(p // 2, p - 1)
        # an easy was of asserting $a \equiv b \pmod{p}$
        b = a + p
        self.assertEqual(legendre(a, p), legendre(b, p))

        p = random_prime(100)
        a = random.randint(p // 2, p - 1)
        b = random.randint(p // 2, p - 1)
        self.assertEqual(legendre(a * b, p), legendre(a, p) * legendre(b, p))

    def test_jacobi_properties(self):
        p = random_prime(5)
        q = random_prime(5)
        n = p * q
        a = random.randint(p // 2, p - 1)
        b = a + n
        self.assertEqual(jacobi(a, n), jacobi(b, n))

    def test_eratosthenes_sieve(self):
        # compare the first 10 primes and the primes under 30
        self.assertSequenceEqual(list(primes(10)), eratosthenes_sieve(30))

    def test_primitive_roots(self):
        self.assertListEqual(list(primitive_roots(11)), [2, 6, 7, 8])
        self.assertListEqual(list(primitive_roots(13)), [2, 6, 7, 11])
        self.assertTrue(is_primitive_root(2, 11))
        self.assertFalse(is_primitive_root(3, 13))

    def test_mod_inverse(self):
        self.assertEqual(mod_inverse(3, 11), 4)
        self.assertEqual(mod_inverse(10, 17), 12)

        p = random_prime(3)
        a = random.randint(1, p - 1)
        a_inv = mod_inverse(a, p)
        self.assertEqual(a * a_inv % p, 1)

    def test_gcd(self):
        self.assertEqual(gcd(54134, 123421), math.gcd(54134, 123421))
        self.assertEqual(gcd(9879873, 89798352), math.gcd(9879873, 89798352))

    def test_mod_sqrt(self):
        self.assertEqual((sqrt_mod(12, 13) ** 2) % 13, 12)
        # A prime % 4 != 3
        p = 508037
        a = 254020
        self.assertEqual(legendre(a, p), 1)
        self.assertEqual(sqrt_mod(a, p), 72452)
        self.assertEqual(pow(72452, 2, p), a)

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
        n = 64
        actual = random_prime(n)
        self.assertEqual(len(str(actual)), n)
        self.assertTrue(is_prime(actual))

    def test_miller_rabin_small_1(self):
        n = 10
        prime = random_prime(n)
        self.assertTrue(is_prime(prime))

    def test_miller_rabin_small_2(self):
        n = 64
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

    def test_solovay_1(self):
        n = 396736894567834589803
        self.assertTrue(is_prime(n, 'solovay-strassen'))

        # Test several psuedo primes and carmichael numbers
        self.assertFalse(is_prime(9, 'solovay-strassen'))
        self.assertFalse(is_prime(561, 'solovay-strassen'))
        self.assertFalse(is_prime(1729, 'solovay-strassen'))
        self.assertFalse(is_prime(2465, 'solovay-strassen'))
        self.assertFalse(is_prime(52633, 'solovay-strassen'))

    def test_solovay_2(self):
        # This test is slow for large primes
        p = random_prime(16)
        self.assertTrue(is_prime(p, 'solovay-strassen'))
        ps = list(primes(20))
        self.assertTrue(all(is_prime(p, 'solovay-strassen') for p in ps))


class NotImplementedTest(unittest.TestCase):
    def test_not_implemented(self):
        self.assertRaises(NotImplementedError, wheel_factorization)
        self.assertRaises(NotImplementedError, sundaram_sieve)


class FactoringTest(unittest.TestCase):
    def test_trial_division_factor(self):
        prime_factors = [13, 13, 19, 37, 113]
        num = product(prime_factors)
        found_factors = factor(num, 'trial-division')
        self.assertCountEqual(prime_factors, found_factors)

    def test_fermat_factor_1(self):
        self.assertCountEqual(factor(10, 'fermat'), [2, 5])
        self.assertCountEqual(factor(9, 'fermat'), [3, 3])
        self.assertCountEqual(factor(333, 'fermat'), [37, 3, 3])

    def test_fermat_factor_2(self):
        prime_factors = [13, 19, 37]
        num = product(prime_factors)
        found_factors = factor(num, 'fermat')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, [13, 19, 37])

        # A random composite number picked from nowhere.
        num = 124987921
        found_factors = factor(num, 'fermat')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, [690541, 181])

    def test_pollard_rho_1(self):
        # Taken from Wikipedia
        num = 8051
        f = factor(num, 'pollard-rho')
        self.assertCountEqual(f, [97, 83])

        prime_factors = [13, 19, 37]
        num = product(prime_factors)
        found_factors = factor(num, 'pollard-rho')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, [13, 19, 37])

    def test_gnu_factor(self):
        # test the toolchain, not the algorithm...
        # A random composite number picked from nowhere.
        num = 124987921
        found_factors = factor(num, 'gnu-factor')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, [690541, 181])

    @unittest.skipIf(sys.version_info[1] < 6 or sys.version_info[0] < 3, 'random.choices new in 3.6')
    def test_pollard_rho_2(self):
        p = list(primes(20))
        prime_factors = random.choices(p, k=5)
        num = product(prime_factors)
        found_factors = factor(num, 'pollard-rho')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, prime_factors)

    def test_pollard_p1(self):
        # Taken from Wikipedia
        num = 8051
        f = factor(num, 'pollard-p1')
        self.assertCountEqual(f, [97, 83])

    @unittest.skipIf(sys.version_info[1] < 6 or sys.version_info[0] < 3, 'random.choices new in 3.6')
    def test_pollard_p1_2(self):
        p = list(primes(10))
        prime_factors = random.choices(p, k=5)
        num = product(prime_factors)
        found_factors = factor(num, 'pollard-p1')
        self.assertEqual(num, product(found_factors))
        self.assertCountEqual(found_factors, prime_factors)


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
