import numpy
from crypto.classical import AffineCipher
from crypto.math import SymbolFrequencies, coprimes
from crypto.utilities import int_mapping


class AffineAttack(object):
    """
        Implements two strategies to attack an Affine Cipher.

        1. A naive frequency attack that assumes the top three most common letters are 'e', 'a', and
           't' respectively. The attack then solve a linear system to find the key.

        2. A Brute force attack that returns an iterator of decrypted potential plaintexts for the
           user to manipulate. This ends up working quite well because there are only 312 possible
           keys to use with the Affine Cipher.
    """

    def __init__(self, ciphertext):
        """
            Construct an affine cipher attack given some large ciphertext

            Example:

            >>> from crypto.classical import AffineCipher
            >>> cipher = AffineCipher(9, 18)
            >>> ciphertext = cipher.encrypt('This is a test')
            >>> attack = AffineAttack(ciphertext)
        """
        self.ciphertext = ''.join(ciphertext)
        self.frequencies = SymbolFrequencies(self.ciphertext)

    def naive_frequency(self):
        """
            Executes a symbol frequency attack. Assumes the most common plaintext symbols
            are `e`, `a`, and `t` respectively.

            Example:

            >>> # demonstrates usage and naivette
            >>> from crypto.classical import AffineCipher
            >>> cipher = AffineCipher(9, 18)
            >>> ciphertext = cipher.encrypt('This is not a test')
            >>> attack = AffineAttack(ciphertext)
            >>> attack.naive_frequency()
            'estdtdyzelepde'
            >>> # above not equal to 'thisisatest' because 't' is the most common character
        """
        # TODO: The doctest for this function randomly failed with the plaintext 'This is a test'.
        #       Occaisionally it would compute the (alpha, beta) pair as (20, 22), which is weird...
        most_common = self.frequencies.most_common(3)
        b1 = int_mapping(most_common[0][0])
        # Pick `e` and `t` over `e` and `a` so that the matrix is invertible mod 26.
        b3 = int_mapping(most_common[2][0])
        b = numpy.matrix([[b1], [b3]])
        # Hard code the matrix inverse. The word 'naive' *is* in the function name...
        m_inverse = numpy.matrix([[19, 7], [3, 24]])
        x = numpy.transpose(numpy.mod(m_inverse * b, 26)).tolist()[0]
        cipher = AffineCipher(*x)
        return cipher.decrypt(self.ciphertext)

    def brute_force(self):
        """
            Yields the results of a brute force attack on all possible keys one by one. Yields
            tuples of the form (decrypted text, a, b).

            Example:

            >>> from crypto.classical import AffineCipher
            >>> affine = AffineCipher(9, 18)
            >>> c = affine.encrypt('This is a test')
            >>> attack = AffineAttack(c)
            >>> b = attack.brute_force()
            >>> for p, a, b in b:
            ...     if p.startswith('this'):
            ...         print(a, b, p)
            9 18 thisisatest
        """
        for a in coprimes(26):
            for b in range(26):
                cipher = AffineCipher(a, b)
                yield cipher.decrypt(self.ciphertext), a, b
