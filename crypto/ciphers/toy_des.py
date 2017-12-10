import string
from crypto.utilities import TextBitstream, lazy_pad
from crypto.utilities import bits_to_integer, xor_streams, bits_of
from .des import DesChunker


class ToyDesCipher(object):
    """
        Implements a toy version of the DES cipher as described in class and the textbook.

        On each round, L_i and R_i are 6 bits, while K_i is 8 bits.
    """

    # The (in)famous S-boxes
    _S1 = [[(1, 0, 1), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 0)],
           [(0, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 0, 1), (0, 1, 1)]]
    _S2 = [[(1, 0, 0), (0, 0, 0), (1, 1, 0), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
           [(1, 0, 1), (0, 1, 1), (0, 0, 0), (1, 1, 1), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0)]]

    def __init__(self, key, number_of_rounds=4):
        """
            Takes the lowest 9 bits of the given `key` and runs `number_of_rounds` of the Feistel
            System on the messages to be encrypted.
        """
        # bits_of yields bits LSBF, want to store MSBF to be consistent with the book
        self.key = tuple(bits_of(key, 9))[::-1]
        self.number_of_rounds = number_of_rounds

    @classmethod
    def expand_bits(cls, bitstring):
        """
            Expands a 6 - bit bitstring into an 8 - bit bitstring

            Example:

            >>> ToyDesCipher.expand_bits([0, 1, 1, 0, 0, 1])
            [0, 1, 0, 1, 0, 1, 0, 1]
            >>> ToyDesCipher.expand_bits([1, 0, 0, 1, 1, 0])
            [1, 0, 1, 0, 1, 0, 1, 0]
        """
        if len(bitstring) != 6:
            raise ValueError('`bitstring` must be 6 bits')
        else:
            return [bitstring[i] for i in [0, 1, 3, 2, 3, 2, 4, 5]]

    @classmethod
    def S1(cls, bits):
        """
            Returns the S1-box value associated with the given bits

            Example:
            >>> ToyDesCipher.S1((1, 1, 1, 1))
            (0, 1, 1)
        """
        return cls._S1[bits[0]][bits_to_integer(reversed(bits[1:]))]

    @classmethod
    def S2(cls, bits):
        """
            Returns the S2-box value associated with the given bits

            Example:
            >>> ToyDesCipher.S2((1, 1, 1, 1))
            (1, 0, 0)
        """
        return cls._S2[bits[0]][bits_to_integer(reversed(bits[1:]))]

    @classmethod
    def f(cls, R, K):
        """
            The encryption function `f` in the DES algorithm

            Example:

            >>> ToyDesCipher.f([1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 0, 1])
            (0, 0, 0, 1, 0, 0)
        """
        bits = tuple(xor_streams(cls.expand_bits(R), K))
        # Concatenate the output of the S-boxes.
        return cls.S1(bits[:4]) + cls.S2(bits[4:])

    @classmethod
    def rotate(cls, key, i):
        """
            The ToyDesCipher key rotation function as defined in the book. Note that the given index
            is one-indexed, not zero.

            Example:

            >>> ToyDesCipher.rotate([0, 1, 0, 0, 1, 1, 0, 0, 1], 4)
            [0, 1, 1, 0, 0, 1, 0, 1]
            >>> ToyDesCipher.rotate([0, 1, 0, 0, 1, 1, 0, 0, 1], 3)
            [0, 0, 1, 1, 0, 0, 1, 0]
            >>> ToyDesCipher.rotate([0, 0, 1, 0, 0, 1, 1, 0, 1], 2)
            [0, 1, 0, 0, 1, 1, 0, 1]
            >>> ToyDesCipher.rotate([0, 0, 1, 0, 0, 1, 1, 0, 1], 1)
            [0, 0, 1, 0, 0, 1, 1, 0]
        """
        if i == 1:
            return key[:8]
        i -= 1
        return key[i:] + key[:i - 1]

    def feistel_round(self, L, R, i):
        """
            Runs one round of the Feistel System on the given chunk

            Example:

            >>> cipher = ToyDesCipher(0b010011001)
            >>> cipher.feistel_round((0, 1, 1, 1, 0, 0), (1, 0, 0, 1, 1, 0), 4)
            ((1, 0, 0, 1, 1, 0), (0, 1, 1, 0, 0, 0))
        """
        K = self.rotate(self.key, i)
        return R, tuple(xor_streams(L, self.f(R, K)))

    def encrypt_chunk(self, chunk, rounds=None):
        """
            Runs the Feistel System rounds on a single (L, R) chunk to encrypt it.

            Will accept a list of round numbers to enable starting in the middle of the algorithm.

            Example:
            >>> cipher = ToyDesCipher(0b001001101)
            >>> L1R1 = ((0, 0, 0, 1, 1, 1), (0, 1, 1, 0, 1, 1))
            >>> L1R1S = ((1, 0, 1, 1, 1, 0), (0, 1, 1, 0, 1, 1))
            >>> cipher.encrypt_chunk(L1R1, rounds=[2, 3, 4])
            ((0, 0, 0, 0, 1, 1), (1, 0, 0, 1, 0, 1))
            >>> cipher.encrypt_chunk(L1R1)  # Treat L1R1 as L0R0 and run all four rounds.
            ((0, 1, 0, 1, 1, 1), (0, 0, 0, 1, 0, 0))
            >>> cipher.encrypt_chunk(L1R1S, rounds=[2, 3, 4])
            ((1, 0, 0, 1, 0, 0), (0, 1, 1, 0, 0, 0))
        """
        L, R = chunk
        for i in range(1, self.number_of_rounds + 1) if rounds is None else rounds:
            L, R = self.feistel_round(L, R, i)
        return L, R

    def encrypt_chunks(self, chunker):
        """Given a chunker, yield encrypted chunk after encrypted chunk"""
        for chunk in chunker:
            yield self.encrypt_chunk(chunk)

    def encrypt(self, message):
        """Encrypts the given message with the DES cipher."""
        # Pad the message to ensure that there is the right number of bits in the message
        message = lazy_pad(message, 3, string.printable)
        # Convert the message to a bitstream.
        bitstream = TextBitstream(message)
        # Chunk the bitstream into 12 bit chunks --> a tuple (L, R) of 6 bit bitstrings.
        chunker = DesChunker(bitstream, 6)
        # Lazily encrypt chunk after chunk.
        encrypter = self.encrypt_chunks(chunker)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(encrypter)

    def decrypt_chunk(self, chunk):
        """Runs the Feistel System rounds on a single (L, R) chunk to decrypt it."""
        # Swap L and R
        R, L = chunk
        # Run the feistel rounds as in encryption, but with keys going from n..1
        for i in range(self.number_of_rounds, 0, -1):
            L, R = self.feistel_round(L, R, i)
        # Swap L and R
        return R, L

    def decrypt_chunks(self, chunker):
        """Given a chunker, yield decrypted chunk after decrypted chunk"""
        for chunk in chunker:
            yield self.decrypt_chunk(chunk)

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext with the DES cipher."""
        # Pad the ciphertext to ensure that there is the right number of bits in the ciphertext
        ciphertext = lazy_pad(ciphertext, 3, string.printable)
        # Convert the ciphertext to a bitstream.
        bitstream = TextBitstream(ciphertext)
        # Chunk the bitstream into 12 bit chunks --> a tuple (L, R) of 6 bit bitstrings.
        chunker = DesChunker(bitstream, 6)
        # Lazily decrypt chunk after chunk
        decrypter = self.decrypt_chunks(chunker)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(decrypter)
