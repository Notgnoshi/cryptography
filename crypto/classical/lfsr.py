from crypto.random import LinearFeedbackShiftRegister
from crypto.utilities import Bitstream, TextBitstream, bits_to_bytes, xor_streams


class LfsrCipher(object):
    """Implements a classical Linear Feedback Shift Register Cipher."""

    def __init__(self, initial_values, coeffs):
        # Need two identical key streams because you cannot retrieve values after
        # the stream has been consumed. This means that messages must be encrypted and
        # decrypted in the same order.
        self.encode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)
        self.decode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)

    def encrypt(self, message):
        """Encrypts the given message with a LFSR Cipher."""
        message_stream = TextBitstream(message)
        cipher_bits = xor_streams(message_stream, self.encode_key_stream)

        return ''.join(map(chr, bits_to_bytes(cipher_bits)))

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext with a LFSR Cipher."""
        # Cannot use TextBitstream because of preprocessing...
        cipher_stream = Bitstream(ord(c) for c in ciphertext)
        cipher_bits = xor_streams(cipher_stream, self.decode_key_stream)

        return ''.join(map(chr, bits_to_bytes(cipher_bits)))
