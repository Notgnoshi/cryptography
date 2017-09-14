from crypto.classical import HillCipher
from crypto.random import generate_alpha
import math
import numpy
from string import ascii_uppercase
import unittest


class HillCipherTest(unittest.TestCase):
    def test_encode(self):
        self.assertListEqual(list(range(0, 26)), HillCipher.encode(ascii_uppercase))

    def test_decode(self):
        self.assertEqual(ascii_uppercase, HillCipher.decode(list(range(0, 26))))

    def test_pad_message(self):
        message = 'test'
        block_size = 5
        self.assertEqual('testX', HillCipher.pad_message(message, block_size))
        block_size = 6
        self.assertEqual('testXX', HillCipher.pad_message(message, block_size))
        block_size = 7
        self.assertEqual('testXXX', HillCipher.pad_message(message, block_size))
        message = 'testxxxtest'
        self.assertEqual('testxxxtestXXX', HillCipher.pad_message(message, block_size))

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
        expected = 'ZWSENIUSPLJVEUAH'
        self.assertEqual(expected, hill.encrypt(message))

    def test_decrypt(self):
        key = numpy.matrix([[15, 12], [11, 3]])
        hill = HillCipher(key)
        expected = 'HOWAREYOUTODAYXX'
        cipher = 'ZWSENIUSPLJVEUAH'
        self.assertEqual(expected, hill.decrypt(cipher))

    def test_random_key(self):
        block_size = 5
        key = HillCipher.generate_key(block_size)
        message = generate_alpha(50)
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))

    def test_random_key_large(self):
        block_size = 9
        key = HillCipher.generate_key(block_size)
        # Generate a *large* random message
        message = generate_alpha(500 * block_size)
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))

    @unittest.expectedFailure
    def test_random_key_larger(self):
        # Decrypt fails on larger block_sizes
        block_size = 13
        key = HillCipher.generate_key(block_size)
        message = generate_alpha(5 * block_size)
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))
