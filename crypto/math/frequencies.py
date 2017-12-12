"""
Defines a SymbolFrequencies calculator for implementing frequency analysis based attacks.
"""

from collections import Counter
from operator import itemgetter


class SymbolFrequencies(Counter):
    """
        Calculates a symbol frequency table from a given iterable

        Examples:
        >>> symbols = 'aabc'
        >>> table = SymbolFrequencies(symbols)
        >>> assert table == {'a': 2, 'b': 1, 'c': 1}
        >>> assert table.proportions == {'a': 0.5, 'b': 0.25, 'c': 0.25}  # nice easy numbers...
        >>> symbols = [1, 1, 2, 3]
        >>> table = SymbolFrequencies(symbols)
        >>> assert table == {1: 2, 2: 1, 3: 1}
        >>> assert table.proportions == {1: 0.5, 2: 0.25, 3: 0.25}
    """

    # From Wikipedia, in percent.
    ENGLISH_LETTER_FREQUENCIES = {
        'a': 0.08167,
        'b': 0.01492,
        'c': 0.02782,
        'd': 0.04253,
        'e': 0.12702,
        'f': 0.02228,
        'g': 0.02015,
        'h': 0.06094,
        'i': 0.06966,
        'j': 0.00153,
        'k': 0.00772,
        'l': 0.04025,
        'm': 0.02406,
        'n': 0.06749,
        'o': 0.07507,
        'p': 0.01929,
        'q': 0.00095,
        'r': 0.05987,
        's': 0.06327,
        't': 0.09056,
        'u': 0.02758,
        'v': 0.00978,
        'w': 0.02360,
        'x': 0.00150,
        'y': 0.01974,
        'z': 0.00074,
    }

    def __init__(self, iterable):
        """
            Construct a SymbolFrequencies table from a given iterable

            Example:
            >>> # The following are all equivalent
            >>> symbols = 'aabc'
            >>> symbols = ['a', 'a', 'b', 'c']
            >>> symbols = (c for c in 'aabc')
            >>> table = SymbolFrequencies(symbols)
        """
        # Call the parent Counter constructor.
        super().__init__(iterable)
        # Total number of symbols.
        self.total = sum(self.values())
        # Allow same syntax for counts as for proportions.
        self.counts = self
        # Calculate the proportions of each symbol.
        self.proportions = {key: value / self.total for key, value in self.items()}

    def __repr__(self):
        """
            The official string representation of the frequency table
        """
        rep = 'symbol:\tcount:\tproportion:\n'
        for key, value in sorted(self.items(), key=itemgetter(1), reverse=True):
            rep += '{}\t{}\t{}\n'.format(key, value, value / self.total)
        return rep
