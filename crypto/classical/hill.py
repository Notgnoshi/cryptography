import math
import numpy
from crypto.utilities import nslice, int_mapping, char_mapping, preprocess
from crypto.math import modular_matrix_inverse


class HillCipher(object):
    """
        Implements a classical Hill Cipher.

        The Hill Cipher is one of the first examples of a block cipher, where a one character change
        in the input produces more than one character change in the output and vice versa.

        The Hill Cipher works by splitting the given message into blocks which it then multiplies by
        the key matrix to encrypt the message.

        Decryption works much the same way, except we use the key matrix's modular_matrix_inverse
        to multiply each cipehrtext block.
    """

    def __init__(self, key=None, block_size=5, alphabet_size=26):
        """
            Constructs a HillCipher object from an optional key and block size. Will generate its
            own random key if one is not given. The key may be accessed as the `self.key` property.
        """
        # Generate a key if one is not given.
        self.key = key if key is not None else self.generate_key(block_size, alphabet_size)
        # Infer the block_size if the key was passed in.
        self.block_size, _ = self.key.shape
        self.alphabet_size = alphabet_size
        self.key_inverse = modular_matrix_inverse(self.key, self.alphabet_size)
        self.fill_value = 'x'

    @staticmethod
    def generate_key(block_size, alphabet_size=26):
        """
            Generate the Hill cipher matrix key by generating random matrices until it finds one
            with a determinant invertible mod the alphabet_size.

            This method hangs when given large block sizes. The largest usable block size seems
            to be 11.

            Example:

            >>> key = HillCipher.generate_key(4)
        """
        # Create a random matrix from 0 to N that is nxn
        M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        # The determinant of an integer matrix is an integer
        # This loop seems not to terminate if the block size is large
        while math.gcd(int(round(numpy.linalg.det(M))), alphabet_size) != 1:
            M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        return M

    @staticmethod
    def encode(string):
        """
            Encodes an alphabetic string such that a:0, b:1, c:2, ...

            Example:

            >>> HillCipher.encode('abc')
            [0, 1, 2]
        """
        return [int_mapping(c) for c in string]

    @staticmethod
    def decode(nums):
        """
            Decodes a numeric list such that 0:a, 1:b, 2:c, ...

            Example:

            >>> HillCipher.decode([0, 1, 2])
            'abc'
        """
        return ''.join(char_mapping(int(n)) for n in nums)

    def encrypt(self, message):
        """
            Encrypts a the given message using the Hill Cipher.

            Example:

            >>> key = numpy.matrix([[15, 12], [11, 3]])
            >>> cipher = HillCipher(key)
            >>> cipher.encrypt('howareyoutodayx')
            'zwseniuspljveuah'
        """
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
        """
            Decrypts the given ciphertext using the Hill Cipher.

            Example:

            >>> key = numpy.matrix([[15, 12], [11, 3]])
            >>> cipher = HillCipher(key)
            >>> cipher.decrypt('zwseniuspljveuah')
            'howareyoutodayxx'
        """
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
