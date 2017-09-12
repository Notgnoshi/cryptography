from collections import deque
from crypto.utilities import Bitstream, Bitfield
from crypto.utilities import nslice
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
        # Need two identical key streams because you cannot retrieve values after
        # the stream has been consumed.
        self.encode_key_stream = Lfsr(initial_values, coeffs)
        self.decode_key_stream = Lfsr(initial_values, coeffs)

    def xor_key(self, bits, key_stream):
        """Returns an XORd bitstream of the inputted bit sequence and key stream."""
        return (k ^ int(b) for k, b in zip(key_stream, bits))

    def encrypt(self, message):
        """Encrypts the given message with a LFSR Cipher."""
        message_stream = Bitstream(message)
        cipher_bits = self.xor_key(message_stream, self.encode_key_stream)

        return ''.join(chr(Bitfield.bits_to_integer(byte)) for byte in nslice(cipher_bits, 8))

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext with a LFSR Cipher."""
        cipher_stream = Bitstream(ciphertext)
        cipher_bits = self.xor_key(cipher_stream, self.decode_key_stream)

        return ''.join(chr(Bitfield.bits_to_integer(byte)) for byte in nslice(cipher_bits, 8))
