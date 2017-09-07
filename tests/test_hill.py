from crypto import HillCipher, Passwords
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

    def test_generate_key(self):
        block_size = 7
        key = HillCipher.generate_key(block_size)
        cipher = HillCipher(key)
        self.assertListEqual(key.tolist(), cipher.key.tolist())
        self.assertEqual(block_size, key.shape[0])
        self.assertEqual(block_size, cipher.block_size)

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
        block_size = 7
        key = HillCipher.generate_key(block_size)
        # Generate random 49 character string
        message = Passwords.gen_alpha(49)
        hill = HillCipher(key)
        cipher = hill.encrypt(message)
        self.assertEqual(message, hill.decrypt(cipher))
