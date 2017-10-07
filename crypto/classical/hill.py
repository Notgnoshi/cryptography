from crypto.utilities import nslice, int_mapping, char_mapping, preprocessor
from crypto.math import modular_matrix_inverse
import gmpy2
import math
import numpy


class HillCipher(object):
    """Implements a classical Hill Cipher."""

    def __init__(self, key=None, block_size=5, alphabet_size=26):
        self.key = key if key is not None else self.generate_key(block_size, alphabet_size)
        self.block_size, _ = key.shape
        self.alphabet_size = alphabet_size
        self.fill_value = 'X'

    @classmethod
    def generate_key(cls, block_size, alphabet_size=26):
        """Generate the Hill cipher matrix key"""
        # Create a random matrix from 0 to N that is nxn
        M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        # The determinant of an integer matrix is an integer
        # This loop seems not to terminate if the block size is large
        while math.gcd(int(round(numpy.linalg.det(M))), alphabet_size) != 1:
            M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        return M

    @classmethod
    def encode(cls, string):
        """Encodes an alphabetic string such that A:0, B:1, C:2, ..."""
        return [int_mapping(c.upper()) for c in string]

    @classmethod
    def decode(cls, nums):
        """Decodes a numeric list such that 0:A, 1:B, 2:C, ..."""
        return ''.join(char_mapping(int(n)) for n in nums).upper()

    @classmethod
    def pad_message(cls, message, block_size):
        """Pads a message with enough 'X's to produce full blocks."""
        # If the message length is evenly divisible by the block size, don't pad.
        if len(message) % block_size == 0:
            return message

        return message + 'X' * (block_size - (len(message) % block_size))

    def encrypt(self, message):
        """Encrypts a the given message using the Hill Cipher."""

        coded_blocks = []
        for block in nslice(preprocessor(message), self.block_size, self.fill_value):
            nums = numpy.matrix(self.encode(block))
            coded_blocks.append(numpy.mod(numpy.matmul(nums, self.key), self.alphabet_size))

        cipher = ''
        for block in coded_blocks:
            cipher += self.decode(numpy.nditer(block))

        return cipher

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext using the Hill Cipher."""
        m_inv = modular_matrix_inverse(self.key, self.alphabet_size)

        decoded_blocks = []
        for block in nslice(ciphertext, self.block_size, self.fill_value):
            nums = numpy.matrix(self.encode(block))
            decoded_blocks.append(numpy.mod(numpy.matmul(nums, m_inv), self.alphabet_size))

        text = ''
        for block in decoded_blocks:
            text += self.decode(numpy.nditer(block))

        return text
