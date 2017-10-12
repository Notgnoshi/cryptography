from crypto.utilities import *
from crypto.classical import HillCipher
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

    def __init__(self, key, number_of_rounds=3):
        """Takes the key as a bitstring '10001010'"""
        if len(key) != 9:
            raise ValueError('key must be a 9-bit sequence of 1\'s and 0\'s')
        self.key = [bool(bit) for bit in key]
        self.number_of_rounds = number_of_rounds

    @classmethod
    def expand_bits(cls, bitstring):
        """Expands a 6 - bit bitstring into an 8 - bit bitstring"""
        if len(bitstring) != 6:
            raise ValueError('`bitstring` must be 6 bits')
        else:
            return [bitstring[i] for i in [0, 1, 3, 2, 3, 2, 4, 5]]

    def _S1(self, bits):
        """Returns the S1-box value associated with the given bits"""
        return self.S1[bits[0]][bits_to_integer(bits[1:])]

    def _S2(self, bits):
        """Returns the S2-box value associated with the given bits"""
        return self.S1[bits[0]][bits_to_integer(bits[1:])]

    def _f(self, R, K):
        """The encryption function `f` in the DES algorithm"""
        bits = tuple(xor_streams(self.expand_bits(R), K))
        # Concatenate the output of the S-boxes.
        return self._S1(bits[:4]) + self._S2(bits[4:])

    def feistel_round(self, L, R, i):
        """Runs one round of the Feistel System on the given chunk"""
        K = wrap_around(self.key, i)
        return R, tuple(xor_streams(L, self._f(R, K)))

    def _encrypt_chunk(self, chunk):
        """Runs the Feistel System rounds on a single (L, R) chunk to encrypt it."""
        L, R = chunk
        for i in range(1, self.number_of_rounds + 1):
            L, R = self.feistel_round(L, R, i)
        return L, R

    def _encrypt_chunks(self, chunker):
        """Given a chunker, yield encrypted chunk after encrypted chunk"""
        for chunk in chunker:
            yield self._encrypt_chunk(chunk)

    def encrypt(self, message):
        """Encrypts the given message with the DES cipher."""
        # Pad the message to ensure that there is the right number of bits in the message
        message = HillCipher.pad_message(''.join(preprocess(message)), 3)
        # Convert the message to a bitstream.
        bitstream = TextBitstream(message)
        # Chunk the bitstream into 12 bit chunks --> a tuple (L, R) of 6 bit bitstrings.
        chunker = DesChunker(bitstream, 6)
        # Lazily encrypt chunk after chunk.
        encryptor = self._encrypt_chunks(chunker)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(encryptor)

    def _decrypt_chunk(self, chunk):
        """Runs the Feistel System rounds on a single (L, R) chunk to decrypt it."""
        # Swap L and R
        R, L = chunk
        # Run the feistel rounds as in encryption, but with keys going from n..1
        for i in range(self.number_of_rounds, 0, -1):
            L, R = self.feistel_round(L, R, i)
        # Swap L and R
        return R, L

    def _decrypt_chunks(self, chunker):
        """Given a chunker, yield decrypted chunk after decrypted chunk"""
        for chunk in chunker:
            yield self._decrypt_chunk(chunk)

    def decrypt(self, ciphertext):
        """Decrypts the given message with the DES cipher."""
        # Convert the message to a bitstream.
        bitstream = TextBitstream(ciphertext)
        # Chunk the bitstream into 12 bit chunks --> a tuple (L, R) of 6 bit bitstrings.
        chunker = DesChunker(bitstream, 6)
        # Lazily decrypt chunk after chunk
        decryptor = self._decrypt_chunks(chunker)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(decryptor)
