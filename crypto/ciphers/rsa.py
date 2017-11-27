import string
from crypto.utilities import nslice, lazy_pad, preprocess, int_mapping, char_mapping


# TODO: how to use this, if even necessary?
class RsaChunker(object):
    """
        A utility class to chunk a message inputted to the RSA algorithm into blocks of size < n.
    """

    def __init__(self, chunk_size):
        """Creates a chunker to yield piece ofter piece of the given message"""
        self.chunk_size = chunk_size

    def chunker(self, m):
        """
            Chunker implementation.
        """

        for c in nslice(lazy_pad(m, self.chunk_size, string.ascii_lowercase), self.chunk_size):
            yield BaseRsaCipher.str2num(''.join(c))

    @staticmethod
    def dechunker(chunker):
        """
            Converts sequence of integers into a sequence of strings
        """
        for num in chunker:
            yield BaseRsaCipher.num2str(num)


class BaseRsaCipher(object):
    """
        A base RSA cipher that encrypts and decrypts numbers that are less than the encryption
        modulus n.
    """

    def __init__(self, n, e, d):
        self.n = n
        self.e = e
        self.d = d

    def encrypt_number(self, number):
        """
            Encrypts the given number that is less than n.
        """
        assert number < self.n
        return pow(number, self.e, self.n)

    def decrypt_number(self, number):
        """
            Decrypts the given numerical ciphertext.
        """
        return pow(number, self.d, self.n)

    @staticmethod
    def str2num(s):
        """
            Converts the given string to a numerical representation.

            Example:

            >>> BaseRsaCipher.str2num('cat')
            30120
            >>> BaseRsaCipher.str2num('C A t')
            30120
        """
        # The wrong way:
        # return int(''.join(str(int_mapping(c) + 1).zfill(2) for c in s))
        # The right way:
        n = 0
        for c in preprocess(s):
            n *= 100
            n += int_mapping(c) + 1
        return n

    # TODO: This fails on output numbers like 113535859035722866
    @staticmethod
    def num2str(n):
        """
            Converts the given number to a string.

            Example:

            >>> BaseRsaCipher.num2str(30120)
            'cat'
        """
        s = ''
        while n:
            bottom_two = n % 100
            n //= 100
            s += char_mapping(bottom_two - 1)

        # The above reads in the string in reverse order
        return s[::-1]


class RsaCipher(BaseRsaCipher):
    """
        Implements the RSA encryption algorithm
    """
    def __init__(self, n, e, d):
        """
            Constructs an RsaCipher object given the modulus n, which must be a product of two
            primes, encryption exponent e, and decryption exponent d.

            Note that ed = 1 mod (p-1)(q-1) where n = pq.
        """
        super().__init__(n, e, d)
        self.chunk_size = 3

    def encrypt_chunks(self, chunker):
        """
            Yields encrypted chunk after encrypted chunk.
        """
        for num in chunker:
            yield self.encrypt_number(num)

    def decrypt_chunks(self, chunker):
        """
            Yields decrypted chunk after decrypted chunk.
        """
        for num in chunker:
            yield self.decrypt_number(num)

    # TODO: Output a number or string?
    def encrypt(self, message):
        """
            Encrypts the given message
        """
        return self.encrypt_number(self.str2num(message))

    # TODO: Input a number or string?
    def decrypt(self, ciphertext):
        """
            Decrypts the given ciphertext
        """
        return self.num2str(self.decrypt_number(ciphertext))
