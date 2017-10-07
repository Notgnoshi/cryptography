from crypto.utilities import int_mapping, char_mapping, preprocess
import gmpy2


class AffineCipher(object):
    """Implements a classical Affine Cipher"""

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.a_inverse = gmpy2.invert(a, 26)

    def _encrypt_chr(self, character):
        """Numerically encrypts a single given character."""
        return (self.a * int_mapping(character) + self.b) % 26

    def _encrypt_str(self, message):
        """Numerically encrypts a given message, returning a generator of encrypted numbers."""
        return (self._encrypt_chr(character) for character in message)

    def _decrypt_chr(self, character):
        """Numerically decrypts a single given character."""
        return self.a_inverse * (int_mapping(character) - self.b) % 26

    def _decrypt_str(self, cipher):
        """Numerically decrypts a given message, returning a generator of decrypted numbers."""
        return (self._decrypt_chr(character) for character in cipher)

    def encrypt(self, message):
        """Textually encrypts a given message."""
        return ''.join(char_mapping(num) for num in self._encrypt_str(preprocess(message)))

    def decrypt(self, cipher):
        """Textually decrypts a given ciphertext."""
        return ''.join(char_mapping(num) for num in self._decrypt_str(cipher))
