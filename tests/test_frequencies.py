from crypto.math import SymbolFrequencies as sf
import unittest


class SymbolFrequencyTest(unittest.TestCase):
    def test_counts(self):
        symbols = 'aaaabbbb'
        expected = {'a': 4, 'b': 4}
        actual = sf(symbols)
        self.assertEqual(actual, expected)

    def test_proportions(self):
        symbols = 'aaaabbbb'
        expected = {'a': 1 / 2, 'b': 1 / 2}
        actual = sf(symbols).proportions
        self.assertEqual(actual, expected)

    def test_symbol_filter(self):
        def key(symbol):
            return symbol in 'abc'

        symbols = 'aaaabbbbccccdddd'
        expected = {'a': 4, 'b': 4, 'c': 4}
        actual = sf(symbols, filter_key=key)
        self.assertEqual(actual, expected)
