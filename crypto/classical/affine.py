import gmpy2
import string


class AffineCipher(object):
    """Implements a classical Affine Cipher"""

    def __init__(self, a, b, modulus=26, alphabet=string.ascii_lowercase):
        self.a = a
        self.b = b
        self.modulus = modulus
        self.a_inverse = gmpy2.invert(a, self.modulus)

        # Lookup tables for letters and numbers
        self.LETTER_TABLE = dict(zip(alphabet, range(0, modulus + 1)))
        self.NUMBER_TABLE = dict(zip(range(0, modulus + 1), alphabet))

    def _encrypt_chr(self, character):
        """Numerically encrypts a single given character."""
        return (self.a * self.LETTER_TABLE[character] + self.b) % self.modulus

    def _encrypt_str(self, message):
        """Numerically encrypts a given message, returning a generator of encrypted numbers."""
        return (self._encrypt_chr(character) for character in message)

    def _decrypt_chr(self, character):
        """Numerically decrypts a single given character."""
        return self.a_inverse * (self.LETTER_TABLE[character] - self.b) % self.modulus

    def _decrypt_str(self, cipher):
        """Numerically decrypts a given message, returning a generator of decrypted numbers."""
        return (self._decrypt_chr(character) for character in cipher)

    def encrypt(self, message):
        """Textually encrypts a given message."""
        return ''.join(self.NUMBER_TABLE[num] for num in self._encrypt_str(message.lower()))

    def decrypt(self, cipher):
        """Textually decrypts a given ciphertext."""
        return ''.join(self.NUMBER_TABLE[num] for num in self._decrypt_str(cipher))
