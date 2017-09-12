from crypto.classical import Lfsr, LfsrCipher
import itertools
import numpy
import unittest


class LsfrTest(unittest.TestCase):
    def test_recurrence_1(self):
        # Values taken from textbook, pages 45-46.
        initial_values = numpy.array([0, 1, 1, 0])
        coeffs = numpy.array([1, 1, 0, 0])
        lfsr = Lfsr(initial_values, coeffs)

        expected = [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1]
        actual = list(itertools.islice(lfsr, len(expected)))
        self.assertListEqual(actual, expected)

    def test_recurrence_2(self):
        # Values taken from HW 1 problem 6
        initial_values = numpy.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
                                      0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1,
                                      0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0,
                                      1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1,
                                      0, 0, 0, 0, 1, 1, 1, 0, 0, 0])
        coeffs = numpy.array([1, 1, 0, 1, 1, 0])
        lfsr = Lfsr(initial_values[:6], coeffs)

        expected = initial_values.tolist()
        actual = list(itertools.islice(lfsr, len(expected)))
        self.assertListEqual(actual, expected)


class LfsrCipherTest(unittest.TestCase):
    def test_xor_bits(self):
        # Values taken from textbook, page 44.
        initial_values = numpy.array([0, 1, 0, 0, 0])
        coeffs = numpy.array([1, 0, 1, 0, 0])
        cipher = LfsrCipher(initial_values, coeffs)

        # Make sure the generated key is the same as in the book.
        lfsr = Lfsr(initial_values, coeffs)
        expected = list(int(b) for b in '01000010010110011111000110111010100001001011001111')
        actual = list(itertools.islice(lfsr, len(expected)))
        self.assertListEqual(actual, expected)

        # Test the actual bitwise XOR of the key and the given plaintext.
        actual = list(cipher.xor_key('1011001110001111'))
        expected = list(int(b) for b in '1111000111010110')
        self.assertSequenceEqual(actual, expected)
