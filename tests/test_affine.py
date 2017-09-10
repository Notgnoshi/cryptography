from crypto.classical import AffineCipher
import math
import random
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
