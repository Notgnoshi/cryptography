from collections import Counter
from operator import itemgetter


class SymbolFrequencies(Counter):
    """Calculates a symbol frequency table from a given iterable"""

    def __init__(self, iterable, filter_key=str.isalpha):
        # Call the parent Counter constructor.
        super().__init__(filter(filter_key, iterable))
        # Total number of symbols.
        self.total = sum(self.values())
        # Allow same syntax for counts as for proportions.
        self.counts = self
        # Calculate the proportions of each symbol.
        self.proportions = {key: value / self.total for key, value in self.items()}

    def __repr__(self):
        """The official string representation of the frequency table"""
        rep = 'symbol:\tcount:\tproportion:\n'
        for key, value in sorted(self.items(), key=itemgetter(1), reverse=True):
            rep += '{}\t{}\t{}\n'.format(key, value, value / self.total)
        return rep
