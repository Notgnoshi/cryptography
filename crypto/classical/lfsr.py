from collections import deque
from crypto.utilities import Bitstream
import numpy


class Lfsr(object):
    """A Linear Feedback Shift Register."""
    def __init__(self, initial_values, coeffs):
        self.initial_values = deque(initial_values)
        self.current_values = initial_values
        self.coeffs = coeffs

    def __iter__(self):
        """Returns an infinite sequence generator"""
        return self

    def __next__(self):
        """
            Returns the next item in the sequence. Starts yielding values beginning
            with the first given initial value.
        """

        # Consume the initial values before moving on to generating new ones.
        if self.initial_values:
            return self.initial_values.popleft()

        next_element = numpy.mod(numpy.dot(self.coeffs, self.current_values), 2)
        self.current_values = numpy.append(self.current_values[1:], next_element)

        return next_element


class LfsrCipher(object):
    """Implements a classical Linear Feedback Shift Register Cipher."""
    def __init__(self, initial_values, coeffs):
        self.key_stream = Lfsr(initial_values, coeffs)

    def xor_key(self, bits):
        """Returns a binary string of the inputted binary string XORd with the key stream."""
        return ''.join(str(k ^ int(b)) for k, b in zip(self.key_stream, bits))

    def encrypt(self, message):
        """Encrypts the given message with a LFSR Cipher."""
        message_stream = Bitstream(message)
        cipher_bits = [m ^ k for m, k in zip(self.key_stream, message_stream)]

    def decrypt(self, cipher):
        """Decrypts the given ciphertext with a LFSR Cipher."""
        pass

    # @classmethod
    # def bytes_xor(cls, a, b):
    #     """Returns a bitwise XOR of two inputed bytes() objects"""
    #     return bytes(x ^ y for x, y in zip(a, b))
