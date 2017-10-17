from crypto.classical import AffineCipher
from crypto.math import SymbolFrequencies
from crypto.utilities import int_mapping
import numpy


class AffineAttack(object):
    """Implements a strategy to attack an Affine Cipher."""

    def __init__(self, ciphertext):
        """Construct an affine cipher attack given some large ciphertext"""
        self.ciphertext = ''.join(ciphertext)
        self.frequencies = SymbolFrequencies(self.ciphertext)

    def naive_frequency_attack(self):
        """
            Executes a symbol frequency attack. Assumes the most common plaintext symbols
            are `e`, `a`, and `t` respectively.
        """
        most_common = self.frequencies.most_common(3)
        b1 = int_mapping(most_common[0][0])
        # Pick `e` and `t` over `e` and `a` so that the matrix is invertible mod 26.
        b3 = int_mapping(most_common[2][0])
        b = numpy.matrix([[b1], [b3]])
        m_inverse = numpy.matrix([[19, 7], [3, 24]])
        x = numpy.transpose(numpy.mod(m_inverse * b, 26)).tolist()[0]
        cipher = AffineCipher(*x)
        return cipher.decrypt(self.ciphertext)
