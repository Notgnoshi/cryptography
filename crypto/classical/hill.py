from crypto.utilities import nslice, int_mapping, char_mapping, preprocess
from crypto.math import modular_matrix_inverse
import gmpy2
import math
import numpy


class HillCipher(object):
    """Implements a classical Hill Cipher."""

    def __init__(self, key=None, block_size=5, alphabet_size=26):
        # Generate a key if one is not given.
        self.key = key if key is not None else self.generate_key(block_size, alphabet_size)
        # Infer the block_size if the key was passed in.
        self.block_size, _ = self.key.shape
        self.alphabet_size = alphabet_size
        self.key_inverse = modular_matrix_inverse(self.key, self.alphabet_size)
        self.fill_value = 'x'

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
        """Encodes an alphabetic string such that a:0, b:1, c:2, ..."""
        return [int_mapping(c) for c in string]

    @classmethod
    def decode(cls, nums):
        """Decodes a numeric list such that 0:a, 1:b, 2:c, ..."""
        return ''.join(char_mapping(int(n)) for n in nums)

    @classmethod
    def pad_message(cls, message, block_size):
        """Pads a message with enough 'x's to produce full blocks."""
        return message + 'x' * ((block_size - len(message)) % block_size)

    def encrypt(self, message):
        """Encrypts a the given message using the Hill Cipher."""
        blocks = []
        # Convert the message into blocks with the given fill value to make them evenly divisible.
        for block in nslice(preprocess(message), self.block_size, self.fill_value):
            block = numpy.matrix(self.encode(block))
            blocks.append(numpy.mod(numpy.matmul(block, self.key), self.alphabet_size))

        # Convert the numerically encrypted text to a string.
        ciphertext = ''
        for block in blocks:
            ciphertext += self.decode(numpy.nditer(block))

        return ciphertext

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext using the Hill Cipher."""
        blocks = []
        # Encrypted text should have evenly divisible blocks, but if not, avoid a crash by filling.
        for block in nslice(ciphertext, self.block_size, self.fill_value):
            block = numpy.matrix(self.encode(block))
            blocks.append(numpy.mod(numpy.matmul(block, self.key_inverse), self.alphabet_size))

        # Convert the numerically decrypted text to a string.
        plaintext = ''
        for block in blocks:
            plaintext += self.decode(numpy.nditer(block))

        return plaintext
