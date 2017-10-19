from itertools import cycle
from crypto.utilities import int_mapping, char_mapping, preprocess


class VigenereCipher(object):
    """Implements a classical Vigenere Cipher."""

    def __init__(self, key):
        self.key = [int_mapping(k) for k in key]

    def encrypt(self, message):
        """Encrypts the given message using a Vigenere Cipher"""
        E = (((k + int_mapping(c)) % 26) for k, c in zip(cycle(self.key), preprocess(message)))
        return ''.join(char_mapping(n) for n in E)

    def decrypt(self, cipher):
        """Decrypts the given ciphertext using a Vigenere Cipher"""
        D = (((int_mapping(c) - k) % 26) for k, c in zip(cycle(self.key), cipher))
        return ''.join(char_mapping(n) for n in D)
