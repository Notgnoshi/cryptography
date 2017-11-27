import string
import numpy
from crypto.utilities import rotate, max_pair, char_mapping
from crypto.math import SymbolFrequencies


class VigenereAttack(object):
    """
        Implements a strategy to attack a Vigenere Cipher by finding the key length and then
        the key using a method described in the textbook.
    """

    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

    @staticmethod
    def coincidences(original, rotation):
        """
            Compares a rotated ciphertext with the original ciphertext and counts how many
            character coincidences there are for the given rotation.

            The following text and rotation:

                aaabbb
                aabbba

            has four coincidences:

                AAaBBb
                AAbBBa

            Example:

            >>> VigenereAttack.coincidences('abcddd', 'bcddda')
            2
            >>> VigenereAttack.coincidences('aaabbb', 'aabbba')
            4
            >>> VigenereAttack.coincidences('aabba', 'abbaa')
            3
        """

        return sum(o == r for o, r in zip(original, rotation))

    @classmethod
    def compare_rotations(cls, text):
        """
            Counts the coincidences of all rotations of the given text.

            Returns a dictionary of rotation : coincidences pairs

            Example:

            >>> VigenereAttack.compare_rotations('abcddd')
            {1: 2, 2: 1, 3: 0, 4: 1, 5: 2}
            >>> VigenereAttack.compare_rotations('aaabbb')
            {1: 4, 2: 2, 3: 0, 4: 2, 5: 4}
        """

        return {r: cls.coincidences(text, rotate(text, -r)) for r in range(1, min(15, len(text)))}

    def probable_key_length(self):
        """
            Computes the probable key length by comparing rotations of the ciphertext to the
            original ciphertext and counting the coincidences. The maximum number of coincidences
            is the probable key length.
        """
        max_coincidence, _ = max_pair(self.compare_rotations(self.ciphertext))
        return max_coincidence

    def probable_key(self):
        """
            Attempts to find the key by performing a frequency analysis on every
            `probable_key_length`th character and performing the second method for finding the
            key as described in the textbook.

            Assume the key length is known to be n and A_0 is the known English Letter Frequenceies:

            for i in 1..n:
                * Compute the frequencies of the filtered letters in positions i mod n
                * for j in 1..25 compute W dot A_j where A_j is A_0 rotated right j positions
                * k_i = the j associated with the maximum dot product in the previous step
            The key is then probably {k_1, ..., k_n}
        """

        def proportion_vector(proportions):
            """
                Produces a proportions vector from a SymbolFrequencies.proportions object. Necessary
                because the proportions object is a dictionary with keys that have proportions > 0.
            """

            vec = []
            for c in string.ascii_lowercase:
                try:
                    vec.append(proportions[c])
                except KeyError:
                    vec.append(0)
            return numpy.array(vec)

        # Convert ENGLISH_LETTER_FREQUENCIES.values() to an array rather than a dict.view() object
        A0 = numpy.array([SymbolFrequencies.ENGLISH_LETTER_FREQUENCIES[l] for l in string.ascii_lowercase])

        key_length = self.probable_key_length()
        key = []
        for i in range(0, key_length):
            # Filter the ciphertext and calculate the symbol frequencies
            table = SymbolFrequencies(self.ciphertext[i::key_length])
            W = proportion_vector(table.proportions)
            # numpy.roll is equivalent to crypto.utilities.rotate, but returns a numpy.array
            # Find the alphabet index associated with the maximum dot product
            ki, _ = max_pair({j: numpy.dot(W, numpy.roll(A0, j)) for j in range(0, 26)})
            key.append(ki)

        return ''.join(map(char_mapping, key))
