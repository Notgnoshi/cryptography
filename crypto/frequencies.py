from collections import Counter


class SymbolFrequencies(Counter):
    """Calculates a symbol frequency table from a given iterable"""
    def __init__(self, iterable, filter_key=str.isalpha):
        super().__init__(filter(filter_key, iterable))
        total = sum(self.values())
        # Allow same syntax for counts as for proportions
        self.counts = self
        self.proportions = {key: value / total for key, value in self.items()}
