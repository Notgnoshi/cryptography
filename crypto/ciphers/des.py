from crypto.utilities import *


class DesChunker(object):
    """
        A class to chunk a bitstream for the DES cipher into chunks (L, R) of a given
        chunk size.
    """

    def __init__(self, bitstream, chunk_size):
        """Creates a chunker, to return tuples (L, R) where L and R have the specified chunk size"""
        self.chunker = self._chunker(bitstream, chunk_size)

    def _chunker(self, bitstream, chunk_size):
        """
            Chunker implementation. Requires the bitstream to have a number of bits evenly
            divisible by 2 * `chunk_size`
        """

        for chunk in nslice(bitstream, 2 * chunk_size):
            yield chunk[:chunk_size], chunk[chunk_size:]

    def __iter__(self):
        """Returns the chunker generator"""
        return self.chunker

    def __next__(self):
        """Returns the next chunk in the chunker"""
        return next(self.chunker)

    @classmethod
    def chunks_to_bitstream(cls, chunker):
        """Converts a sequence of (L, R) chunks into a bitstream"""
        for L, R in chunker:
            # Yield the left bits
            for bit in L:
                yield bit
            # and then the right bits.
            for bit in R:
                yield bit

    @classmethod
    def chunks_to_string(cls, chunker):
        """Converts a sequence of (L, R) chunks into a string"""
        return bits_to_string(cls.chunks_to_bitstream(chunker))


class DesCipher(object):
    """Defines the DES cipher."""

    def __init__(self):
        raise NotImplementedError('DesCipher has not yet been implemented.')
