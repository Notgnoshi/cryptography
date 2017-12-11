import math
import random
import string
import gmpy2
from crypto.random import random_prime
from crypto.utilities import nslice, lazy_pad, preprocess, int_mapping, char_mapping


class RsaChunker(object):
    """
        A utility class to chunk a message inputted to the RSA algorithm into blocks of size < n.
    """

    def __init__(self, message, chunk_size):
        """Creates a chunker to yield piece ofter piece of the given message"""
        self.stream_chunker = self.chunker(message, chunk_size)

    @staticmethod
    def chunker(m, chunk_size):
        """
            Chunker implementation. Converts the message to a series of numbers.
        """
        for c in nslice(lazy_pad(m, chunk_size, string.ascii_lowercase), chunk_size):
            yield BaseRsaCipher.str2num(''.join(c))

    def __iter__(self):
        """Returns the chunker generator"""
        return self.stream_chunker

    def __next__(self):
        """Returns the next chunk in the chunker"""
        return next(self.stream_chunker)


class BaseRsaCipher(object):
    """
        A base RSA cipher that encrypts and decrypts numbers that are less than the encryption
        modulus n.

        The BaseRsaCipher is necessary to simplify the implementation of the complete RsaCipher,
        that encrypts and decrypts strings.
    """

    def __init__(self, n, e, d):
        self.n = n
        self.e = e
        self.d = d

    def encrypt_number(self, number):
        """
            Encrypts the given number that is less than n. Implements RSA encryption on numbers.

            Returns the given number raised to the encryption exponent, mod n.
        """
        assert number < self.n
        return pow(number, self.e, self.n)

    def decrypt_number(self, number):
        """
            Decrypts the given numerical ciphertext. Implements RSA decryption on numbers.

            Returns the given number raised to the decryption exponent, mod n.
        """
        return pow(number, self.d, self.n)

    @staticmethod
    def str2num(s):
        """
            Converts the given string to a numerical representation. Each letter gets mapped to a
            number, then each left-zero-padded number gets concatenated together to form a number
            representation of the given string.

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
            Converts the given number to a string by taking the number two digits at a time,
            starting from the least significant digits and working up, converting each chunk to a
            letter.

            Note that not every number corresponds to a string.

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
        Implements the RSA encryption algorithm. Works by chunking the given message into a series
        of numbers, each of which is independently encrypted by the RSA algorithm before being
        concatenated together to form the ciphertext.
    """

    def __init__(self, n, e, d):
        """
            Constructs an RsaCipher object given the modulus n, which must be a product of two
            primes, encryption exponent e, and decryption exponent d.

            Note that n, e, and d must be known beforehand.

            Note that ed = 1 mod (p-1)(q-1) where n = pq.
        """
        super().__init__(n, e, d)
        self.chunk_size = (n.bit_length() // 8) // 2

    def encrypt_chunks(self, chunker):
        """
            Yields encrypted chunk after encrypted chunk. Each chunk will be a bytes() object.
        """
        for num in chunker:
            e = self.encrypt_number(num)
            b = e.to_bytes(e.bit_length() // 8 + 1, 'little')
            yield b

    def decrypt_chunks(self, chunker):
        """
            Yields decrypted chunk after decrypted chunk. The chunker must be an iterable of
            encrypted bytes() objects.
        """
        for b in chunker:
            yield self.num2str(self.decrypt_number(int.from_bytes(b, 'little')))

    def encrypt(self, message):
        """
            Encrypts the given message. Returns an iterator of bytes() objects.

            Example:

            >>> cipher = RsaCipher(885320963 * 238855417, 9007, 116402471153538991)
            >>> ciphertext = cipher.encrypt('thisisatest')
            >>> type(ciphertext)
            <class 'generator'>
            >>> encrypted_bytes = next(ciphertext)
            >>> type(encrypted_bytes)
            <class 'bytes'>
            >>> encrypted_bytes
            b'A\\x1f\\x93\\x81\\x9bs\\xf1\\x01'
        """
        # Yields chunked number after number
        chunker = RsaChunker(preprocess(message), self.chunk_size)
        # Yields encrypted bytes() after bytes()
        return self.encrypt_chunks(chunker)

    def decrypt(self, ciphertext):
        """
            Decrypts the given ciphertext. Takes in an iterator of encrypted bytes() objects,
            and returns a string of the decrypted plaintext.

            Example:

            >>> cipher = RsaCipher(885320963 * 238855417, 9007, 116402471153538991)
            >>> ciphertext = cipher.encrypt('thisisatestx')
            >>> plaintext = cipher.decrypt(ciphertext)
            >>> type(plaintext)
            <class 'str'>
            >>> plaintext
            'thisisatestx'
        """

        # Takes an iterator of encrypted bytes() and joins the decrypted text
        return ''.join(self.decrypt_chunks(ciphertext))


class RsaKeyGenerator(object):
    """
        Generates the public and corresponding private keys for RsaCipher. The key generator works
        by generating two random primes of the given size, which guarantees that `n` will be at
        least as big as the specified size.
    """

    def __init__(self, bit_size):
        """
            Given the bit size of the RSA key, construct a RsaKeyGenerator, which will generated a
            key at least as big as the specified key size.
        """
        self.p = random_prime(bit_size)
        self.q = random_prime(bit_size)
        self.n = self.p * self.q
        self.e = 0
        self.d = 0
        self.limit = (self.p - 1) * (self.q - 1)
        self.public_key = self.gen_public_key()
        self.private_key = self.gen_private_key()

    def gen_public_key(self):
        """
            Generates the RSA public key (n, e) by generating random numbers until it finds one
            that is relatively prime with (p - 1)(q - 1).
        """
        while math.gcd(self.e, self.limit) != 1:
            # Prefer large encryption exponents
            self.e = random.randint(self.limit // 3, self.limit)

        return self.n, self.e

    def gen_private_key(self):
        """
            Generates the RSA private key (decryption exponent) d by computing the multiplicative
            inverse of the encryption exponent modulo (p - 1)(q - 1).
        """
        self.d = int(gmpy2.invert(self.e, self.limit))
        return self.d
