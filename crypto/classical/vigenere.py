from itertools import cycle
from crypto.utilities import int_mapping, char_mapping, preprocess


class VigenereCipher(object):
    """
        Implements a classical Vigenere Cipher.

        The Vigenere Cipher uses a cyclic key ('abc' --> 'abcabcabc...') which gets added (mod 26)
        to the plaintext characterwise to encrypt it.

        To decrypt, the cipher subtracts the key characterwise.

        Example:

        >>> cipher = VigenereCipher('thisisakey')
        >>> cipher.encrypt('thisisatest')
        'moqkqkadiqm'
        >>> cipher.decrypt('moqkqkadiqm')
        'thisisatest'
    """

    def __init__(self, key):
        """
            Constructs a VigenereCipher from a lowercase ASCII alphabet-only string key

            Example:

            >>> cipher = VigenereCipher('thisisakey')
            >>> cipher = VigenereCipher('This is not a key')
            Traceback (most recent call last):
              File "<stdin>", line 1, in ?
            KeyError: ' '
        """
        self.key = [int_mapping(k) for k in key]

    def encrypt(self, message):
        """
            Encrypts the given message using a Vigenere Cipher

            Example:

            >>> cipher = VigenereCipher('key')
            >>> cipher.encrypt('message')
            'wiqceeo'
        """
        E = (((k + int_mapping(c)) % 26) for k, c in zip(cycle(self.key), preprocess(message)))
        return ''.join(char_mapping(n) for n in E)

    def decrypt(self, cipher):
        """
            Decrypts the given ciphertext using a Vigenere Cipher

            Example:

            >>> cipher = VigenereCipher('key')
            >>> cipher.decrypt('wiqceeo')
            'message'
        """
        D = (((int_mapping(c) - k) % 26) for k, c in zip(cycle(self.key), cipher))
        return ''.join(char_mapping(n) for n in D)
