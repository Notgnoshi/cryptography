from functools import reduce
from .utils import nslice


def set_ith_bit(num, index, value):
    """
        Sets the ith bit of num to the given value

        Example:

        >>> set_ith_bit(1, 1, 1)
        3
    """
    # https://stackoverflow.com/questions/28360586/setting-nth-bit-of-unsigned-int
    num ^= (-value ^ num) & (1 << index)
    return num


def set_bit(num, bit):
    """
        Sets to ith bit of num to 1

        Example:

        >>> set_bit(1, 1)
        3
    """
    return set_ith_bit(num, bit, 1)


def clear_bit(num, bit):
    """
        Sets the ith bit of num to 0

        Example:
        >>> clear_bit(3, 1)
        1
    """
    return set_ith_bit(num, bit, 0)


def get_bit(num, bit):
    """
        Gets the value of the ith bit of num

        Example:

        >>> get_bit(3, 1)
        1
        >>> get_bit(1, 1)
        0
    """
    return bool((num >> bit) & 1)


def bits_of(value, bits=None):
    """
        A generator to iterate over `bits` bits of the given value starting from the least
        significant bit to the most significant bit.

        Example:

        >>> list(bits_of(3, 4))  # 0b0011
        [1, 1, 0, 0]
    """
    bits = value.bit_length() if bits is None else bits
    for i in range(bits):
        yield (value >> i) & 1


def binary_string(string):
    """
        Returns the binary representation of a string, lsbf

        Example:

        >>> binary_string('a')
        '10000110'
    """
    return ''.join('{0:08b}'.format(ord(x), 'b')[::-1] for x in string)


def bits_to_integer(seq):
    """
        Converts a sequence of bits into a integer

        Example:

        >>> bits_to_integer([1, 1, 0, 0])
        3
    """
    integer = 0
    for i, bit in enumerate(seq):
        integer = set_ith_bit(integer, i, bit)

    return integer


def bits_to_bytes(bitstream):
    """
        Converts a bitstream to a bytestream. Requires the length of the bitstream (which need not
        be known) to be a multiple of 8.

        Examples:

        >>> bits = [1, 1, 1, 1, 0, 0, 0, 0]  # 0b00001111 = 15
        >>> bytes = bits_to_bytes(bits)
        >>> next(bytes)
        15

        Results in a failure if the length of the bitstream is not divisible by 8:

        >>> bits = [1, 1, 1, 1, 0, 0, 0]
        >>> len(bits)
        7
        >>> bytes = bits_to_bytes(bits)
        >>> next(bytes)
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for <<: 'NoneType' and 'int'
    """
    # Reverse the eight_bits to account for endianness
    return (reduce(lambda byte, bit: byte << 1 | bit, reversed(eight_bits)) for eight_bits in nslice(bitstream, 8))


def bytes_to_string(bytestream):
    """
        Converts a bytestream to a string

        Example:

        >>> string = b'abcd'
        >>> bytes_to_string(string)
        'abcd'
    """
    return ''.join(map(chr, bytestream))


def bits_to_string(bitstream):
    """
        Converts a bitstream to a string. Due to implementation, bits_to_string has the same
        problem related to bitstream length being divisible by 8 as bits_to_bytes has.

        Example:

        >>> bits = [1, 0, 0, 0, 0, 1, 1, 0]
        >>> bits_to_string(bits)
        'a'
        >>> bits_to_string([1, 1, 1])
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for <<: 'NoneType' and 'int'
    """
    return bytes_to_string(bits_to_bytes(bitstream))


def xor_streams(bitstream1, bitstream2):
    """
        Bitwise XORs two bitstreams

        Example:

        >>> a = [1, 0, 1, 1]
        >>> b = [0, 0, 1, 1]
        >>> list(xor_streams(a, b))
        [1, 0, 0, 0]
    """
    return (l ^ r for l, r in zip(bitstream1, bitstream2))


class Bitstream(object):
    """
        Turns an iterable of bytes into a bit-by-bit bitstream of its lsbf binary representation.

        Example:

        >>> bitstream = Bitstream(b'abc')
        >>> list(bitstream)
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0]

        >>> bitstream = Bitstream(ord(c) for c in 'abc')
        >>> list(bitstream)
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0]
    """

    def __init__(self, bytestream):
        """
            Convert the given bytestream to a bitstream. The given bytestream may take on any number
            of forms:

            >>> # The following are equivalent
            >>> bytestream = b'abc'
            >>> bytestream = bytes('abc', 'ascii')
            >>> bytestream = (ord(c) for c in 'abc')
            >>> bytestream = map(ord, 'abc')
            >>> bytestream = bytearray('abc', 'ascii')
            >>> bytestream = [97, 98, 99]
            >>> # They all work the same:
            >>> bitstream = Bitstream(bytestream)
        """
        self.bits = self._bits(bytestream)

    def _bits(self, bytestream):
        """A generator to yield bit after bit of the bitstream"""
        for byte in bytestream:
            for bit in bits_of(byte, 8):
                yield bit

    def __iter__(self):
        """
            Returns the bitstream generator to iterate over.

            Example:

            >>> bitstream = Bitstream(b'abc')
            >>> sum = 0
            >>> for bit in bitstream:
            ...     sum += bit
            >>> sum  # There are 10 True bits in the bitstream.
            10
        """
        return self.bits

    def __next__(self):
        """
            Get the next bit of the bitstream

            Example:

            >>> bitstream = Bitstream(b'abc')
            >>> next(bitstream)
            1
            >>> next(bitstream)
            0
        """
        return next(self.bits)


class TextBitstream(Bitstream):
    """
        Turns an iterable of characters into a Bitstream. As with Bitstream, the iterable may be of
        many forms. Usually it will be some kind of lazily evaluated generator rather than a single
        string or array defined all at once.

        Example:

        >>> # The following are all equivalent
        >>> text = 'abc'
        >>> text = ['a', 'b', 'c']
        >>> text = (c for c in 'abc')  # A dumb example, but useful for large portions of text.
        >>> bitstream1 = TextBitstream(text)
        >>> bitstream2 = Bitstream(b'abc')
        >>> assert list(bitstream1) == list(bitstream2)
    """

    def __init__(self, text):
        """Convert the given text to a bitstream"""
        # Convert a byte sequence of text to a bitstream
        super().__init__(ord(c) for c in text)
