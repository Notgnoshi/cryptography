from crypto.random import generate_alpha
from crypto.utilities import *
from crypto.samples import *
import itertools
import random
import unittest


class PreprocessTest(unittest.TestCase):
    def test_frankenstein(self):
        # Breaking this onto multiple lines breaks the test. Sorry pep8.
        expected = """fromitalytheyvisitedgermanyandfranceitheireldestchildwasbornatnaplesandasaninfantaccompaniedthemintheirramblesiremainedforseveralyearstheironlychildmuchastheywereattachedtoeachothertheyseemedtodrawinexhaustiblestoresofaffectionfromaverymineoflovetobestowthemuponmemymotherstendercaressesandmyfatherssmileofbenevolentpleasurewhileregardingmearemyfirstrecollections"""

        self.assertSequenceEqual(''.join(preprocess(frankenstein_text)), expected)

    def test_unicode(self):
        text = 'ÈÆÖÉEAEOE'
        expected = 'eaeoe'
        self.assertSequenceEqual(''.join(preprocess(text)), expected)

        text = 'ÈÆÖÉEAEOE'
        expected = 'èæöéeaeoe'
        self.assertSequenceEqual(''.join(preprocess(text, use_ascii=False)), expected)


class BitfieldTest(unittest.TestCase):
    byte_array = b'\x53\x61\x6c\x74\x65\x64\x5f\x5f\x1b\x73\xa1\x62'

    def test_bit_generator1(self):
        bits = []
        for bit in bits_of(0b10101100):
            bits.append(bit)

        self.assertListEqual(bits, [0, 0, 1, 1, 0, 1, 0, 1])

    def test_bit_generator2(self):
        bits = []
        for bit in bits_of(self.byte_array[0], bits=4):
            bits.append(bit)

        self.assertListEqual(bits, [1, 1, 0, 0])

    def test_bit_generator3(self):
        bits = []
        for bit in bits_of(0x6153, bits=14):
            bits.append(bit)

        self.assertListEqual(bits, [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1])

    def test_get_bit(self):
        val = 0b10101100
        bits = [get_bit(val, i) for i in range(8)]
        self.assertListEqual(bits, [0, 0, 1, 1, 0, 1, 0, 1])

    def test_set_bit(self):
        val = 0b10101100
        new_val = set_bit(val, 0)
        new_val = set_bit(new_val, 1)

        self.assertEqual(new_val, 0b10101111)

    def test_clear_bit(self):
        val = 0b10101100
        new_val = clear_bit(val, 2)
        new_val = clear_bit(new_val, 3)

        self.assertEqual(new_val, 0b10100000)

    def test_bits_to_integer_1(self):
        bits = [1, 0, 0, 0, 0, 1, 1, 0]
        actual = bits_to_integer(bits)
        expected = 97
        self.assertEqual(actual, expected)

    def test_bits_to_integer_2(self):
        num = random.randint(1, 1000000)
        bits = (int(b) for b in bits_of(num))
        actual = bits_to_integer(bits)
        self.assertEqual(actual, num)

    def test_bits_to_bytes(self):
        string = b'abcd'
        bits = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0,
                0, 1, 1, 0]

        bitstream = Bitstream(string)
        bytestream = bits_to_bytes(bitstream)
        self.assertListEqual(list(bytestream), list(string))

        bytestream = bits_to_bytes(bits)
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
        expected = binary_string(string)
        self.assertSequenceEqual(actual, expected)

    def test_text_bitstream(self):
        string = 'abcd'
        bitstream = TextBitstream(string)
        # abcd in binary lsbf format
        expected = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0,
                    0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

        actual = list(bit for bit in bitstream)
        self.assertListEqual(actual, expected)


class MiscTest(unittest.TestCase):
    def test_rotate(self):
        seq = [1, 2, 3, 4, 5, 6]
        expected = [5, 6, 1, 2, 3, 4]
        actual = rotate(seq, 2)
        self.assertListEqual(actual, expected)

    def test_lazy_pad_1(self):
        # a generator with an odd number of items
        seq = (i for i in [1, 2, 3, 4, 5])
        # chain the generators
        seq = lazy_pad(seq, multiple=2, pad_values='x')
        seq = list(seq)
        # There are an even number of items
        self.assertTrue(len(seq) % 2 == 0)
        # Padded at the end by 'x'
        self.assertListEqual(seq, [1, 2, 3, 4, 5, 'x'])

        # make sure we don't unnecessarily pad
        seq = 'abc'
        seq = lazy_pad(seq, 3, 'xyz')
        self.assertSequenceEqual(''.join(seq), 'abc')

    def test_lazy_pad_2(self):
        seq = 'abcdefg'
        seq = ''.join(lazy_pad(seq, 10, 'X'))
        self.assertSequenceEqual(seq, 'abcdefgXXX')

        # A multiple of 5
        seq = generate_alpha(45)
        # pad the lowercase alphabetic string with numbers chosen at random
        padded_seq = lazy_pad(seq, 7, string.digits)
        for char, padded_char in zip(seq, padded_seq):
            self.assertEqual(char, padded_char)
        for remaining in padded_seq:
            self.assertIn(remaining, string.digits)

    def test_lazy_pad_3(self):
        message = 'test'
        block_size = 3
        self.assertEqual('testxx', ''.join(lazy_pad(message, block_size, 'x')))
        block_size = 4
        self.assertEqual('test', ''.join(lazy_pad(message, block_size, 'x')))
        block_size = 5
        self.assertEqual('testx', ''.join(lazy_pad(message, block_size, 'x')))
        block_size = 6
        self.assertEqual('testxx', ''.join(lazy_pad(message, block_size, 'x')))
        block_size = 7
        self.assertEqual('testxxx', ''.join(lazy_pad(message, block_size, 'x')))
        message = 'testxxxtest'
        self.assertEqual('testxxxtestxxx', ''.join(lazy_pad(message, block_size, 'x')))
