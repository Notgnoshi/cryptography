from crypto.utilities import *
from .des import DesChunker
import itertools


class ToyDesCipher(object):
    """
        Implements a toy version of the DES cipher.

        On each round, L_i and R_i are 6 bits, while K is 8 bits.
    """

    # The (in)famous S-boxes
    S1 = [[(1, 0, 1), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 0)],
          [(0, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 0, 1), (0, 1, 1)]]
    S2 = [[(1, 0, 0), (0, 0, 0), (1, 1, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
          [(1, 0, 1), (0, 1, 1), (0, 0, 0), (1, 1, 1), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0)]]

    def __init__(self, key):
        """Takes the key as a bitstring '10001010'"""
        if len(key) != 9:
            raise ValueError('key must be a 9-bit sequence of 1\'s and 0\'s')
        self.key = [bool(bit) for bit in key]
        self.number_of_rounds = 3

    @classmethod
    def expand_bits(cls, bitstring):
        """Expands a 6 - bit bitstring into an 8 - bit bitstring"""
        if len(bitstring) != 6:
            raise ValueError('`bitstring` must be 6 bits')
        else:
            return [bitstring[i] for i in [0, 1, 3, 2, 3, 2, 4, 5]]

    @classmethod
    def chunks_to_bitstream(cls, chunker):
        """Converts a sequence of (L, R) chunks into a bitstream"""
        # TODO: Move to des.py
        for L, R in chunker:
            # Yield the left bits
            for bit in L:
                yield bit
            # and then the right bits.
            for bit in R:
                yield bit

    @classmethod
    def chunks_to_string(cls, chunker):
        """Converts a sequence of (L, R) chunks into a string"""
        # TODO: Move to des.py
        return bits_to_string(cls.chunks_to_bitstream(chunker))

    def f(self, R, K):
        """The encryption function `f` in the DES algorithm"""
        bits = tuple(xor_streams(self.expand_bits(R), K))
        # TODO: clean this up, and abstract away the S-boxes.
        b1 = bits[:4]
        b2 = bits[4:]
        S1 = self.S1[b1[0]][bits_to_integer(b1[1:])]
        S2 = self.S1[b2[0]][bits_to_integer(b2[1:])]
        return S1 + S2

    def feistel_round(self, L, R, i):
        """Runs one round of the Feistel System on the given chunk"""
        K = wrap_around(self.key, i)
        return R, tuple(xor_streams(L, self.f(R, K)))

    def encrypt_chunk(self, chunk):
        """Runs the Feistel System rounds on a single (L, R) chunk to encrypt it."""
        L0, R0 = chunk
        # TODO: use iteration...
        L1, R1 = self.feistel_round(L0, R0, 1)
        L2, R2 = self.feistel_round(L1, R1, 2)
        L3, R3 = self.feistel_round(L2, R2, 3)

        return L3, R3

    def encrypt_chunks(self, chunker):
        """Given a chunker, yield encrypted chunk after encrypted chunk"""
        for chunk in chunker:
            yield self.encrypt_chunk(chunk)

    def encrypt(self, message):
        """Encrypts the given message with the DES cipher."""
        # TODO: Message padding?
        # Convert the message to a bitstream.
        bitstream = TextBitstream(preprocess(message))
        # Chunk the bitstream into 12 bit chunks --> a tuple (L, R) of 6 bit bitstrings.
        chunker = DesChunker(bitstream, 6)
        # Lazily encrypt chunk after chunk.
        encryptor = self.encrypt_chunks(chunker)
        # Now encode the above generator as a string and return it.
        return self.chunks_to_string(encryptor)

    def decrypt_chunk(self, chunk):
        """Runs the Feistel System rounds on a single (L, R) chunk to decrypt it."""
        R0, L0 = chunk
        # TODO: use iteration...
        L1, R1 = self.feistel_round(L0, R0, 3)
        L2, R2 = self.feistel_round(L1, R1, 2)
        L3, R3 = self.feistel_round(L2, R2, 1)

        return R3, L3

    def decrypt_chunks(self, chunker):
        """Given a chunker, yield decrypted chunk after decrypted chunk"""
        for chunk in chunker:
            yield self.decrypt_chunk(chunk)

    def decrypt(self, ciphertext):
        """Decrypts the given message with the DES cipher."""
        # TODO: Comment.
        bitstream = TextBitstream(ciphertext)
        chunker = DesChunker(bitstream, 6)
        decryptor = self.decrypt_chunks(chunker)
        return self.chunks_to_string(decryptor)
