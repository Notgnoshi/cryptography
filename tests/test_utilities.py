from crypto.random import generate_alpha
from crypto.utilities import *
import random
import unittest


class PreprocessTest(unittest.TestCase):
    def test_frankenstein(self):
        text = """From Italy they visited Germany and France.  I, their eldest child, was
        born at Naples, and as an infant accompanied them in their rambles.  I
        remained for several years their only child.  Much as they were
        attached to each other, they seemed to draw inexhaustible stores of
        affection from a very mine of love to bestow them upon me.  My mother's
        tender caresses and my father's smile of benevolent pleasure while
        regarding me are my first recollections."""

        # Breaking this onto multiple lines breaks the test. Sorry pep8.
        expected = """fromitalytheyvisitedgermanyandfranceitheireldestchildwasbornatnaplesandasaninfantaccompaniedthemintheirramblesiremainedforseveralyearstheironlychildmuchastheywereattachedtoeachothertheyseemedtodrawinexhaustiblestoresofaffectionfromaverymineoflovetobestowthemuponmemymotherstendercaressesandmyfatherssmileofbenevolentpleasurewhileregardingmearemyfirstrecollections"""

        self.assertSequenceEqual(''.join(preprocess(text)), expected)

    def test_unicode(self):
        text = 'ÈÆÖÉEAEOE'
        expected = 'eaeoe'
        self.assertSequenceEqual(''.join(preprocess(text)), expected)

        text = 'ÈÆÖÉEAEOE'
        expected = 'èæöéeaeoe'
        self.assertSequenceEqual(''.join(preprocess(text, ascii=False)), expected)


class BitfieldTest(unittest.TestCase):
    byte_array = b'\x53\x61\x6c\x74\x65\x64\x5f\x5f\x1b\x73\xa1\x62'

    def test_bit_generator1(self):
        bits = []
        for bit in Bitfield.bits(0b10101100):
            bits.append(bit)

        self.assertListEqual(bits, [0, 0, 1, 1, 0, 1, 0, 1])

    def test_bit_generator2(self):
        bits = []
        for bit in Bitfield.bits(self.byte_array[0], bits=4):
            bits.append(bit)

        self.assertListEqual(bits, [1, 1, 0, 0])

    def test_bit_generator3(self):
        bits = []
        for bit in Bitfield.bits(0x6153, bits=14):
            bits.append(bit)

        self.assertListEqual(bits, [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1])

    def test_get_bit(self):
        val = 0b10101100
        bits = [Bitfield.get_bit(val, i) for i in range(8)]
        self.assertListEqual(bits, [0, 0, 1, 1, 0, 1, 0, 1])

    def test_set_bit(self):
        val = 0b10101100
        new_val = Bitfield.set_bit(val, 0)
        new_val = Bitfield.set_bit(new_val, 1)

        self.assertEqual(new_val, 0b10101111)

    def test_clear_bit(self):
        val = 0b10101100
        new_val = Bitfield.clear_bit(val, 2)
        new_val = Bitfield.clear_bit(new_val, 3)

        self.assertEqual(new_val, 0b10100000)

    def test_bits_to_integer_1(self):
        bits = [1, 0, 0, 0, 0, 1, 1, 0]
        actual = Bitfield.bits_to_integer(bits)
        expected = 97
        self.assertEqual(actual, expected)

    def test_bits_to_integer_2(self):
        num = random.randint(1, 1000000)
        bits = (int(b) for b in Bitfield.bits(num))
        actual = Bitfield.bits_to_integer(bits)
        self.assertEqual(actual, num)

    def test_bits_to_bytes(self):
        string = b'abcd'
        bits = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0,
                0, 1, 1, 0]

        bitstream = Bitstream(string)
        bytestream = Bitfield.bits_to_bytes(bitstream)
        self.assertListEqual(list(bytestream), list(string))

        bytestream = Bitfield.bits_to_bytes(bits)
        self.assertListEqual(list(bytestream), list(string))


class BitstreamTest(unittest.TestCase):
    def test_bitstream_types(self):
        # Test equivalent representations of a string. Prefer (ord(c) ...) for large strings.
        strings = [bytes('abcd', 'ascii'), b'abcd', 'abcd'.encode('ascii'), [97, 98, 99, 100],
                   (ord(c) for c in 'abcd'), bytearray('abcd', 'ascii')]
        for string in strings:
            bitstream = Bitstream(string)
            # abcd in binary lsbf format
            expected = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0,
                        0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

            actual = list(bit for bit in bitstream)
            self.assertListEqual(actual, expected)

    def test_bitstream(self):
        string = generate_alpha(1000)
        bitstream = Bitstream(bytes(string, 'ascii'))
        actual = ''.join(str(bit) for bit in bitstream)
        expected = Bitfield.binary_string(string)
        self.assertSequenceEqual(actual, expected)

    def test_text_bitstream(self):
        string = 'abcd'
        bitstream = TextBitstream(string)
        # abcd in binary lsbf format
        expected = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0,
                    0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

        actual = list(bit for bit in bitstream)
        self.assertListEqual(actual, expected)
