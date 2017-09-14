from crypto.utilities import Bitfield, Bitstream
from crypto.random import generate_alpha
import random
import unittest


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


class BitstreamTest(unittest.TestCase):
    def test_bitstream_1(self):
        string = 'abcd'
        bitstream = Bitstream(bytes(string, 'ascii'))
        # abcd in binary lsbf format
        expected = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0,
                    0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

        actual = list(bit for bit in bitstream)
        self.assertListEqual(actual, expected)

    def test_bitstream_2(self):
        string = generate_alpha(1000)
        bitstream = Bitstream(bytes(string, 'ascii'))
        actual = ''.join(str(bit) for bit in bitstream)
        expected = Bitfield.binary_string(string)
        self.assertSequenceEqual(actual, expected)
