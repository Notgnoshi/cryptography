from crypto.random import LinearFeedbackShiftRegister
from crypto.utilities import TextBitstream, bits_to_string, xor_streams, preprocess


class LfsrCipher(object):
    """
        Implements a classical Linear Feedback Shift Register Cipher.

        Uses a Linear Feedback Shift Register to generate pseudorandom numbers in a predictable
        fashion, provided some recurrence relation and initial conditions.

        Encrypts a given bitstream by XORing the bitstream with the LFSR sequence. Decrypts in
        the same manner.

        Example:

        >>> import numpy
        >>> initial_values = numpy.array([1, 0, 1, 0, 0, 1])
        >>> coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        >>> cipher = LfsrCipher(initial_values, coeffs)
        >>> ciphertext = cipher.encrypt('abc')  # Taken from a homework problem
        >>> [ord(c) for c in ciphertext]
        [4, 65, 130]
    """

    def __init__(self, initial_values, coeffs):
        """
            Constructs an LfsrCipher object from numpy vectors defining the initial LFSR values and
            the coefficients of the LFSR recurrence relation.

            Example:

            >>> import numpy
            >>> initial_values = numpy.array([1, 0, 1, 0, 0, 1])
            >>> coeffs = numpy.array([1, 1, 0, 1, 1, 0])
            >>> cipher = LfsrCipher(initial_values, coeffs)
        """
        # Need two identical key streams because you cannot retrieve values after
        # the stream has been consumed. This means that messages must be encrypted and
        # decrypted in the same order.
        self.encode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)
        self.decode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)

    def encrypt(self, message):
        """
            Encrypts the given message with a LFSR Cipher.

            Example:

            >>> import numpy
            >>> initial_values = numpy.array([1, 0, 1, 0, 0, 1])
            >>> coeffs = numpy.array([1, 1, 0, 1, 1, 0])
            >>> cipher = LfsrCipher(initial_values, coeffs)
            >>> cipher.encrypt('abc')
            '\\x04A\\x82'
        """
        message_stream = TextBitstream(preprocess(message))
        cipher_bits = xor_streams(message_stream, self.encode_key_stream)

        return bits_to_string(cipher_bits)

    def decrypt(self, ciphertext):
        """
            Decrypts the given ciphertext with a LFSR Cipher.

            Example:

            >>> import numpy
            >>> initial_values = numpy.array([1, 0, 1, 0, 0, 1])
            >>> coeffs = numpy.array([1, 1, 0, 1, 1, 0])
            >>> cipher = LfsrCipher(initial_values, coeffs)
            >>> cipher.decrypt('\x04A\x82')
            'abc'
        """
        cipher_stream = TextBitstream(ciphertext)
        cipher_bits = xor_streams(cipher_stream, self.decode_key_stream)

        return bits_to_string(cipher_bits)
