from crypto.classical import *
from crypto.random import generate_alpha, LinearFeedbackShiftRegister
from crypto.utilities import *
import itertools
import numpy
import math
import random
import string
import unittest


class AffineCipherTest(unittest.TestCase):
    def test_affine_encrypt(self):
        message = 'affine'
        affine = AffineCipher(9, 2)
        cipher = affine.encrypt(message)
        self.assertEqual(cipher, 'cvvwpm')

    def test_affine_decrypt(self):
        cipher = 'cvvwpm'
        affine = AffineCipher(9, 2)
        self.assertEqual(affine.decrypt(cipher), 'affine')

    def test_coprimes(self):
        message = 'thisisatest'
        # Generate lists of numbers relatively prime with 26.
        lesser_nums = filter(lambda x: math.gcd(x, 26) == 1, range(0, 27))
        greater_nums = filter(lambda x: math.gcd(x, 26) == 1, range(26, 26 * 2))

        # Pairwise iterate over lesser and greater numbers.
        for l, g in zip(lesser_nums, greater_nums):
            shift = random.randrange(0, 27)
            lesser = AffineCipher(l, shift)
            greater = AffineCipher(g, shift)

            l_cipher = lesser.encrypt(message)
            g_cipher = greater.encrypt(message)
            self.assertEqual(l_cipher, g_cipher)


class HillCipherTest(unittest.TestCase):
    def test_encode(self):
        self.assertListEqual(list(range(0, 26)), HillCipher.encode(string.ascii_lowercase))

    def test_decode(self):
        self.assertEqual(string.ascii_lowercase, HillCipher.decode(list(range(0, 26))))

    def test_generate_key_1(self):
        block_size = 7
        alphabet_size = 26
        key = HillCipher.generate_key(block_size, alphabet_size)
        self.assertEqual(math.gcd(int(round(numpy.linalg.det(key))), alphabet_size), 1)

    def test_generate_key_2(self):
        # Block sizes larger than 16 seem to not work, test smaller size for faster tests
        block_size = 13
        alphabet_size = 26
        key = HillCipher.generate_key(block_size, alphabet_size)
        self.assertEqual(math.gcd(int(round(numpy.linalg.det(key))), alphabet_size), 1)

    def test_encrypt(self):
        key = numpy.matrix([[15, 12], [11, 3]])
        hill = HillCipher(key)
        message = 'howareyoutodayx'
        expected = 'zwseniuspljveuah'
        self.assertEqual(expected, hill.encrypt(message))

    def test_decrypt(self):
        key = numpy.matrix([[15, 12], [11, 3]])
        hill = HillCipher(key)
        expected = 'howareyoutodayxx'
        cipher = 'zwseniuspljveuah'
        self.assertEqual(expected, hill.decrypt(cipher))

    def test_random_key(self):
        block_size = 5
        key = HillCipher.generate_key(block_size)
        message = generate_alpha(50).lower()
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))

    def test_random_key_large(self):
        block_size = 9
        key = HillCipher.generate_key(block_size)
        # Generate a *large* random message
        message = generate_alpha(500 * block_size).lower()
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))

    @unittest.expectedFailure
    def test_random_key_larger(self):
        # Decrypt fails on larger block_sizes
        block_size = 13
        key = HillCipher.generate_key(block_size)
        message = generate_alpha(5 * block_size).lower()
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))


class LfsrCipherTest(unittest.TestCase):
    def test_xor_bits_1(self):
        # Values taken from textbook, page 44.
        initial_values = numpy.array([0, 1, 0, 0, 0])
        coeffs = numpy.array([1, 0, 1, 0, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        # Make sure the generated key is the same as in the book.
        lfsr = LinearFeedbackShiftRegister(initial_values, coeffs)
        expected = list(int(b) for b in '01000010010110011111000110111010100001001011001111')
        actual = list(itertools.islice(lfsr, len(expected)))
        self.assertListEqual(actual, expected)

        # Test the actual bitwise XOR of the key and the given plaintext.
        actual = list(xor_streams((int(b) for b in '1011001110001111'), cipher.encode_key_stream))
        expected = list(int(b) for b in '1111000111010110')
        self.assertListEqual(actual, expected)

    def test_xor_bits_2(self):
        # Values taken from HW 1 problem 6
        initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        actual = list(xor_streams((int(b)
                                   for b in '100001100100011011000110'), cipher.encode_key_stream))
        expected = list(int(b) for b in '001000001000001001000001')
        self.assertListEqual(actual, expected)

    def test_encrypt_1(self):
        # Values taken from HW 1 problem 6
        initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        ciphertext = cipher.encrypt('abc')
        actual = [ord(c) for c in ciphertext]
        expected = [4, 65, 130]
        self.assertListEqual(actual, expected)

    def test_encrypt_2(self):
        # Values taken from HW 1 problem 6
        initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        ciphertext = cipher.encrypt('zyxwvuts')
        actual = [ord(c) for c in ciphertext]
        expected = [31, 90, 153, 215, 233, 255, 13, 164]
        self.assertListEqual(actual, expected)

    def test_decrypt_1(self):
        initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        # 'zyxwvuts' encrypted as above
        ciphertext = ''.join(chr(n) for n in [31, 90, 153, 215, 233, 255, 13, 164])
        actual = cipher.decrypt(ciphertext)
        expected = 'zyxwvuts'
        self.assertSequenceEqual(actual, expected)

    def test_encrypt_decrypt_1(self):
        initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        plaintext = string.ascii_lowercase
        ciphertext = cipher.encrypt(plaintext)
        actual = cipher.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, actual)

    def test_encrypt_decrypt_2(self):
        size = 100
        initial_values = numpy.ones(size, dtype=int)
        initial_values[:size // 2] = 0
        numpy.random.shuffle(initial_values)
        coeffs = numpy.ones(size, dtype=int)
        coeffs[:size // 2] = 0
        numpy.random.shuffle(coeffs)

        cipher = LfsrCipher(initial_values, coeffs)
        plaintext = generate_alpha(1000)
        ciphertext = cipher.encrypt(plaintext)
        actual = cipher.decrypt(ciphertext)
        self.assertSequenceEqual(actual, plaintext)


class VigenereCipherTest(unittest.TestCase):
    def test_vigenere_encrypt(self):
        key = 'vector'
        plaintext = 'hereishowitworks'
        expected = 'citxwjcsybhnjvml'
        vigenere = VigenereCipher(key)
        ciphertext = vigenere.encrypt(plaintext)
        self.assertSequenceEqual(ciphertext, expected)

    def test_vigenere_decrypt(self):
        key = 'vector'
        expected = 'hereishowitworks'
        ciphertext = 'citxwjcsybhnjvml'
        vigenere = VigenereCipher(key)
        plaintext = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, expected)

    def test_vigenere_large(self):
        key = 'hereissomerandomkeythaticouldntthinkof'
        vigenere = VigenereCipher(key)
        plaintext = generate_alpha(random.randint(1000, 10000)).lower()
        ciphertext = vigenere.encrypt(plaintext)
        message = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, message)

    def test_vigenere_larger(self):
        key = generate_alpha(random.randint(100, 1000)).lower()
        vigenere = VigenereCipher(key)
        plaintext = generate_alpha(random.randint(10000, 100000)).lower()
        ciphertext = vigenere.encrypt(plaintext)
        message = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, message)
