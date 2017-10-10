from .utils import nslice
from functools import reduce


def set_ith_bit(num, index, value):
    """Sets the ith bit of num to the given value"""
    # https://stackoverflow.com/questions/28360586/setting-nth-bit-of-unsigned-int
    num ^= (-value ^ num) & (1 << index)
    return num


def set_bit(num, bit):
    """Sets to ith bit of num to 1"""
    return set_ith_bit(num, bit, 1)


def clear_bit(num, bit):
    """Sets the ith bit of num to 0"""
    return set_ith_bit(num, bit, 0)


def get_bit(num, bit):
    """Gets the value of the ith bit of num"""
    return bool((num >> bit) & 1)


def bits_of(value, bits=None):
    """A generator to iterate over `bits` bits of the given value"""
    bits = value.bit_length() if bits is None else bits
    for i in range(bits):
        yield (value >> i) & 1


def binary_string(string):
    """Returns the binary representation of a string, lsbf"""
    return ''.join('{0:08b}'.format(ord(x), 'b')[::-1] for x in string)


def bits_to_integer(seq):
    """Converts a sequence of bits into a integer"""
    integer = 0
    for i, bit in enumerate(seq):
        integer = set_ith_bit(integer, i, bit)

    return integer


def bits_to_bytes(bitstream):
    """Converts a bitstream to a bytestream"""
    # Reverse the eight_bits to account for endianness
    return (reduce(lambda byte, bit: byte << 1 | bit, reversed(eight_bits)) for eight_bits in nslice(bitstream, 8))


def bytes_to_string(bytestream):
    """Converts a bytestream to a string"""
    return ''.join(map(chr, bytestream))


def bits_to_string(bitstream):
    """Converts a bitstream to a string"""
    return bytes_to_string(bits_to_bytes(bitstream))


def xor_streams(bitstream1, bitstream2):
    """Bitwise XORs two bitstreams"""
    return (l ^ r for l, r in zip(bitstream1, bitstream2))


class Bitstream(object):
    """Turns an iterable of bytes into a bit-by-bit bitstream of its lsbf binary representation."""

    def __init__(self, bytestream):
        self.bits = self._bits(bytestream)

    def _bits(self, bytestream):
        """A generator to yield bit after bit of the bitstream"""
        for byte in bytestream:
            for bit in bits_of(byte, 8):
                yield bit

    def __iter__(self):
        return self.bits

    def __next__(self):
        return next(self.bits)


class TextBitstream(Bitstream):
    """Turns an iterable of characters into a Bitstream."""

    def __init__(self, text):
        # Convert a byte sequence of text to a bitstream
        super().__init__(ord(c) for c in text)
