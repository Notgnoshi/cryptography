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
        self.key = list(bits_of(key))
        self.number_of_rounds = 3

    @classmethod
    def expand_bits(cls, bitstring):
        """Expands a 6 - bit bitstring into an 8 - bit bitstring"""
        if len(bitstring) != 6:
            raise ValueError('`bitstring` must be 6 bits')
        else:
            return [bitstring[i] for i in [0, 1, 3, 2, 3, 2, 4, 5]]

    def feistel(self, R, K):
        """Implements the encryption function `f`"""
        R = self.expand_bits(R)
        bits = tuple(xor_streams(R, K))
        L4, R4 = bits[:4], bits[4:]
        S1 = self.S1[L4[0]][bits_to_integer(L4[1:])]
        S2 = self.S2[R4[0]][bits_to_integer(R4[1:])]
        return S1 + S2

    def run_round(self, L, R, i, forward):
        """Runs the ith round of the Feistel System"""
        if not forward:
            i = range(self.number_of_rounds - 1, -1, -1)[i]
        key_i = wrap_around(self.key, i)
        L_new = R
        R_new = tuple(xor_streams(L, self.feistel(R, key_i)))
        return L_new, R_new

    def run_rounds(self, L, R, forward=True):
        """Runs the Feistel System rounds on L and R"""
        for round_number in range(self.number_of_rounds):
            L, R = self.run_round(L, R, round_number, forward)
        return L, R

    def encrypt_chunks(self, chunker):
        """Yields a sequence of encrypted bits by running the Feistel System on the given chunks"""
        for L, R in chunker:
            L_encrypted, R_encrypted = self.run_rounds(L, R)
            for bit in itertools.chain(L_encrypted, R_encrypted):
                yield bit

    def encrypt(self, message):
        """Encrypts the given message with the DES cipher."""
        bitstream = TextBitstream(preprocess(message))
        chunker = DesChunker(bitstream, 6)
        return bits_to_string(self.encrypt_chunks(chunker))

    def decrypt_chunks(self, chunker):
        for L, R in chunker:
            L_decrypted, R_decrypted = self.run_rounds(L, R, forward=False)
            for bit in itertools.chain(L_decrypted, R_decrypted):
                yield bit

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext with the DES cipher."""
        bitstream = TextBitstream(ciphertext)
        chunker = DesChunker(bitstream, 6)
        return bits_to_string(self.decrypt_chunks(chunker))
