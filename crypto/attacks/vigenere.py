from crypto.classical import VigenereCipher
from crypto.utilities import rotate, max_pair
from crypto.math import SymbolFrequencies


class VigenereAttack(object):
    """
        Implements a strategy to attack a Vigenere Cipher by finding the key length and then
        the key
    """

    def __init__(self, ciphertext):
        self.ciphertext = ciphertext

    @staticmethod
    def count_coincidences(original, rotation):
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

            >>> VigenereAttack.count_coincidences('abcddd', 'bcddda')
            2
            >>> VigenereAttack.count_coincidences('aaabbb', 'aabbba')
            4
            >>> VigenereAttack.count_coincidences('aabba', 'abbaa')
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

        return {r: cls.count_coincidences(text, rotate(text, -r)) for r in range(1, min(15, len(text)))}

    def probable_key_length(self):
        """
            Computes the probable key length by comparing rotations of the ciphertext to the
            original ciphertext and counting the coincidences. The maximum number of coincidences
            is the probable key length
        """

        return max_pair(self.compare_rotations(self.ciphertext))[0]

    def possible_key(self):
        """
            Attempts to find the key by performing a frequency analysis on every
            `probable_key_length`th character
        """

        key_length = self.probable_key_length()
        for i in range(0, key_length):
            filtered = self.ciphertext[i::key_length]
            table = SymbolFrequencies(filtered)
            print(table.most_common(4))
