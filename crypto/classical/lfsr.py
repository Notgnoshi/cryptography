from crypto.random import LinearFeedbackShiftRegister
from crypto.utilities import Bitstream, Bitfield, nslice


class LfsrCipher(object):
    """Implements a classical Linear Feedback Shift Register Cipher."""

    def __init__(self, initial_values, coeffs):
        # Need two identical key streams because you cannot retrieve values after
        # the stream has been consumed. This means that messages must be encrypted and
        # decrypted in the same order.
        self.encode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)
        self.decode_key_stream = LinearFeedbackShiftRegister(initial_values, coeffs)

    def xor_key(self, bits, key_stream):
        """Returns an XORd bitstream of the inputted bit sequence and key stream."""
        return (k ^ int(b) for k, b in zip(key_stream, bits))

    def encrypt(self, message):
        """Encrypts the given message with a LFSR Cipher."""
        # Convert to integer representation of each character on the fly
        message_stream = Bitstream(ord(c) for c in message)
        cipher_bits = self.xor_key(message_stream, self.encode_key_stream)

        return ''.join(chr(Bitfield.bits_to_integer(byte)) for byte in nslice(cipher_bits, 8))

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext with a LFSR Cipher."""
        # Convert to integer representation of each character on the fly
        cipher_stream = Bitstream(ord(c) for c in ciphertext)
        cipher_bits = self.xor_key(cipher_stream, self.decode_key_stream)

        return ''.join(chr(Bitfield.bits_to_integer(byte)) for byte in nslice(cipher_bits, 8))
