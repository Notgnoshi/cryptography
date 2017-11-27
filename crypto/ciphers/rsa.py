import string
from crypto.utilities import nslice, lazy_pad, preprocess, int_mapping


# TODO: Clean this class up
class RsaChunker(object):
    """
        A utility class to chunk a message inputted to the RSA algorithm into blocks of size < n.
    """

    def __init__(self, chunk_size):
        """Creates a chunker to yield piece ofter piece of the given message"""
        self.chunk_size = chunk_size

    def chunker(self, message):
        """
            Chunker implementation.
        """

        for chunk in nslice(lazy_pad(message, self.chunk_size, string.ascii_lowercase), self.chunk_size):
            # yield int.from_bytes(bytes(''.join(chunk), 'ascii'), byteorder='little')
            # TODO: Test with the book's method of converting strings to numbers, then go back to above for speed
            yield int(''.join(str(int_mapping(c)).zfill(2) for c in chunk))

    def dechunker(self, chunker):
        """
            Converts sequence of integers into a sequence of strings
        """
        for num in chunker:
            # yield num.to_bytes(self.chunk_size, 'little').decode('utf-8')
            yield str(num)


class RsaCipher(object):
    """
        Implements the RSA encryption algorithm
    """
    def __init__(self, n, e, d):
        """
            Constructs an RsaCipher object given the modulus n, which must be a product of two
            primes, encryption exponent e, and decryption exponent d.

            Note that ed = 1 mod (p-1)(q-1) where n = pq.
        """
        self.n = n
        self.e = e
        self.d = d

    def encrypt_chunks(self, chunker):
        """
            Yields encrypted chunk after encrypted chunk.
        """
        for num in chunker:
            yield pow(num, self.e, self.n)

    # TODO: Make a naive encrypter first (one that blindly assumes m < n)
    def encrypt(self, message):
        """
            Encrypts the given message
        """
        # Create a 256 byte message chunker
        # TODO: Chunk size?
        rsachunker = RsaChunker(3)
        chunker = rsachunker.chunker(preprocess(message))
        encrypter = self.encrypt_chunks(chunker)
        # Now convert a series of numbers back into strings
        dechunker = rsachunker.dechunker(encrypter)
        return ''.join(dechunker)
