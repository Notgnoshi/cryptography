from crypto.utilities import int_mapping, char_mapping, preprocess
import gmpy2


class AffineCipher(object):
    """
        Implements a classical Affine Cipher.

        Affine ciphers implements the encryption function Encrypt : plain -> cipher defined by some
        affine multiplication and shift:
            E(m_i) = a * m_i + b (mod 26)

        Note that for this encryption to be reversible, the multiplicative inverse (mod 26) of a
        must exist. Decryption is implemented as the function Decryption : cipher -> plain defined
        by
            D(c_i) = a_inv * (c_i - b) (mod 26)

        Example usage:

        >>> cipher = AffineCipher(9, 18)
        >>> cipher.encrypt('affine')
        'sllmfc'
        >>> cipher.decrypt('sllmfc')
        'affine'
    """

    def __init__(self, a, b):
        """
            Constructs an AffineCipher object with the parameters `a` and `b`. Note that `a` must
            have a multiplicative inverse mod 26.

            Example:

            >>> cipher = AffineCipher(2, 15)
            Traceback (most recent call last):
              File "<stdin>", line 1, in ?
            ValueError: 2 must be invertible mod 26
            >>> cipher = AffineCipher(9, 18)
        """
        self.modulus = 26
        self.a = a
        self.b = b
        try:
            self.a_inverse = gmpy2.invert(a, self.modulus)
        except ZeroDivisionError:
            raise ValueError('{} must be invertible mod {}'.format(self.a, self.modulus))

    def encrypt_chr(self, character):
        """
            Encrypts a single given character by first mapping that character to a number in the
            range 0..25 before numerically encrypting it and mapping it back to a character.

            Example:

            >>> cipher = AffineCipher(9, 18)
            >>> cipher.encrypt_chr('a')
            's'
        """
        return char_mapping((self.a * int_mapping(character) + self.b) % self.modulus)

    def decrypt_chr(self, character):
        """
            Decrypts a single given character by first mapping that character to a number in the
            range 0..25 before numerically decrypting it and mapping it back to a character.

            Example:
            >>> cipher = AffineCipher(9, 18)
            >>> cipher.decrypt_chr('s')
            'a'
        """
        return char_mapping(self.a_inverse * (int_mapping(character) - self.b) % self.modulus)

    def encrypt(self, message):
        """
            Textually encrypts a given message.

            Example:

            >>> cipher = AffineCipher(9, 18)
            >>> cipher.encrypt('affine')
            'sllmfc'
        """
        return ''.join(self.encrypt_chr(character) for character in preprocess(message))

    def decrypt(self, cipher):
        """
            Textually decrypts a given ciphertext.

            Example:

            >>> cipher = AffineCipher(9, 18)
            >>> cipher.decrypt('sllmfc')
            'affine'
        """
        return ''.join(self.decrypt_chr(character) for character in cipher)
