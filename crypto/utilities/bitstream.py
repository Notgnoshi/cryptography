class Bitfield(object):
    """A utility class for bitfield manipulations"""
    @classmethod
    def set_ith_bit(cls, num, index, value):
        """Sets the ith bit of num to the given value"""
        # https://stackoverflow.com/questions/28360586/setting-nth-bit-of-unsigned-int
        num ^= (-value ^ num) & (1 << index)
        return num

    @classmethod
    def set_bit(cls, num, bit):
        """Sets to ith bit of num to 1"""
        return cls.set_ith_bit(num, bit, 1)

    @classmethod
    def clear_bit(cls, num, bit):
        """Sets the ith bit of num to 0"""
        return cls.set_ith_bit(num, bit, 0)

    @classmethod
    def get_bit(cls, num, bit):
        """Gets the value of the ith bit of num"""
        return bool((num >> bit) & 1)

    @classmethod
    def bits(cls, value, bits=None):
        """A generator to iterate over `bits` bits of the given value"""
        bits = value.bit_length() if bits is None else bits
        for i in range(bits):
            yield (value >> i) & 1

    @classmethod
    def binary_string(cls, string):
        """Returns the binary representation of a string, lsbf"""
        return ''.join('{0:08b}'.format(ord(x), 'b')[::-1] for x in string)

    @classmethod
    def bits_to_integer(cls, seq):
        """Converts a sequence of bits into a integer"""
        integer = 0
        for i, bit in enumerate(seq):
            integer = cls.set_ith_bit(integer, i, bit)

        return integer


class Bitstream(object):
    """Turns an ascii string into a bit-by-bit bitstream of its lsbf binary representation."""

    def __init__(self, string):
        self.bitstream = self._bits(bytes(string, 'utf-8'))

    def _bits(self, bytes):
        """A generator to yield bit after bit of the bitstream"""
        for byte in bytes:
            for bit in Bitfield.bits(byte, 8):
                yield bit

    def __iter__(self):
        return self

    def __next__(self):
        """Get the next bit from the bitstream"""
        return next(self.bitstream)
