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
