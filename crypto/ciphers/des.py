import itertools
from crypto.utilities import nslice, rotate, TextBitstream, lazy_pad
from crypto.utilities import bits_to_string, bits_of, bits_to_integer, xor_streams


class DesChunker(object):
    """
        A utility class to chunk a bitstream for the DES cipher into chunks (L, R) of a given
        chunk size.

        Example:

        >>> bitstream = [1, 1, 1, 0, 0, 0]
        >>> chunker = DesChunker(bitstream, 3)
        >>> next(chunker)
        ((1, 1, 1), (0, 0, 0))
    """

    def __init__(self, bitstream, chunk_size):
        """Creates a chunker, to return tuples (L, R) where L and R have the specified chunk size"""
        self.stream_chunker = self.chunker(bitstream, chunk_size)

    @staticmethod
    def chunker(bitstream, chunk_size):
        """
            Chunker implementation. Will pad the given bitstream with 0s if it is not evenly
            divisible by 2*chunk_size.
        """

        for chunk in nslice(lazy_pad(bitstream, 2 * chunk_size), 2 * chunk_size):
            yield chunk[:chunk_size], chunk[chunk_size:]

    def __iter__(self):
        """Returns the chunker generator"""
        return self.stream_chunker

    def __next__(self):
        """Returns the next chunk in the chunker"""
        return next(self.stream_chunker)

    @classmethod
    def chunks_to_bitstream(cls, chunker):
        """
            Converts a sequence of (L, R) chunks into a bitstream

            Example:

            >>> chunker = [((1, 1, 1), (0, 0, 0))]
            >>> list(DesChunker.chunks_to_bitstream(chunker))
            [1, 1, 1, 0, 0, 0]
        """
        for L, R in chunker:
            # Yield the left bits
            for bit in L:
                yield bit
            # and then the right bits.
            for bit in R:
                yield bit

    @classmethod
    def chunks_to_string(cls, chunker):
        """
            Converts a sequence of (L, R) chunks into a string

            Example:

            >>> from crypto.utilities import TextBitstream
            >>> bitstream = TextBitstream('abcdef')
            >>> chunker = DesChunker(bitstream, 6)
            >>> DesChunker.chunks_to_string(chunker)
            'abcdef'
        """
        return bits_to_string(cls.chunks_to_bitstream(chunker))


class DesCipher(object):
    """
        Implements the DES cipher.

        Note that this implementation makes heavy use of *ers: chunkers, permuters, encryptors, etc.
        Each of these *ers accepts some generator, and returns a new generator. This means you can
        track a single chunk through the process in a very straightforward manner.

        >>> cipher = DesCipher(8762323746)
        >>> # Make sure the input is a multiple of 8 for deterministic output
        >>> ciphertext = cipher.encrypt('abcdefgh')
        >>> cipher.decrypt(ciphertext)
        'abcdefgh'
    """

    # Initial permutation table
    _initial_permutation = [57, 49, 41, 33, 25, 17, 9, 1,
                            59, 51, 43, 35, 27, 19, 11, 3,
                            61, 53, 45, 37, 29, 21, 13, 5,
                            63, 55, 47, 39, 31, 23, 15, 7,
                            56, 48, 40, 32, 24, 16, 8, 0,
                            58, 50, 42, 34, 26, 18, 10, 2,
                            60, 52, 44, 36, 28, 20, 12, 4,
                            62, 54, 46, 38, 30, 22, 14, 6]

    # Final permutation (IP^-1) table
    _final_permutation = [39, 7, 47, 15, 55, 23, 63, 31,
                          38, 6, 46, 14, 54, 22, 62, 30,
                          37, 5, 45, 13, 53, 21, 61, 29,
                          36, 4, 44, 12, 52, 20, 60, 28,
                          35, 3, 43, 11, 51, 19, 59, 27,
                          34, 2, 42, 10, 50, 18, 58, 26,
                          33, 1, 41, 9, 49, 17, 57, 25,
                          32, 0, 40, 8, 48, 16, 56, 24]

    # Expand bits table
    _expand_bits = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14,
                    15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27,
                    28, 27, 28, 29, 30, 31, 0]

    # Permutation table for the output of the S-Boxes
    _sbox_permutation = [15, 6, 19, 20, 28, 11,
                         27, 16, 0, 14, 22, 25,
                         4, 17, 30, 9, 1, 7,
                         23, 13, 31, 26, 2, 8,
                         18, 12, 29, 5, 21, 10,
                         3, 24]

    # Key permutation table, filters out the parity bits.
    _key_permutation = [56, 48, 40, 32, 24, 16, 8,
                        0, 57, 49, 41, 33, 25, 17,
                        9, 1, 58, 50, 42, 34, 26,
                        18, 10, 2, 59, 51, 43, 35,
                        62, 54, 46, 38, 30, 22, 14,
                        6, 61, 53, 45, 37, 29, 21,
                        13, 5, 60, 52, 44, 36, 28,
                        20, 12, 4, 27, 19, 11, 3]

    # CD bitstring permutation table
    _CD_permutation = [13, 16, 10, 23, 0, 4,
                       2, 27, 14, 5, 20, 9,
                       22, 18, 11, 3, 25, 7,
                       15, 6, 26, 19, 12, 1,
                       40, 51, 30, 36, 46, 54,
                       29, 39, 50, 44, 32, 47,
                       43, 48, 38, 55, 33, 52,
                       45, 41, 49, 35, 28, 31]

    # The (in)famous S-boxes.
    _sbox = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
    ]

    def __init__(self, key):
        """
            Constructs a DesCipher object. Takes in the first 64 bits of the given `key` and
            generates the subkeys in a 1-indexed array in `self.keys`. Note that the initial key
            permutation discards the parity bits.

            Example:

            >>> key = 1476123957612341  # More than 64 bits. The cipher will use the first 64 bits.
            >>> cipher = DesCipher(key)
            >>> ciphertext = cipher.encrypt('messageX')
            >>> cipher.decrypt(ciphertext)
            'messageX'
        """

        def keys(key, num_rounds):
            """Yields the permuted key bitstring for i = 1..num_rounds"""
            C, D = key[:28], key[28:]
            # Rounds are 1-indexed, so shift array over by one
            left_shifts = [None, 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
            for i in range(1, num_rounds + 1):
                # Negate each rotation to rotate left.
                C, D = rotate(C, -left_shifts[i]), rotate(D, -left_shifts[i])
                yield self.permute(C + D, self._CD_permutation)

        self.key = list(bits_of(key, 64))
        # Permute the key. The permutation discards the parity bits...
        self.key = self.permute(self.key, self._key_permutation)
        self.number_of_rounds = 16
        # A list of the 16 keys K1 .. K16, shifted over by one to allow 1-indexing.
        self.keys = [None] + list(keys(self.key, self.number_of_rounds))

    @classmethod
    def expand_bits(cls, bits):
        """
            Expands a 32 bit bitstring into a 48 bit bitstring as indicated by the DES algorithm

            Will only accept a precomputed bitstring, not a lazily evaluated one. This is because
            the bitstring must be indexible by the permutation.

            Example:

            >>> bits = [0] * 32
            >>> expanded = DesCipher.expand_bits(bits)
            >>> expanded == [0] * 48
            True
            >>> bits = tuple(bits_of(0x123456789, 32))
            >>> DesCipher.expand_bits(bits)
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        """
        if len(bits) != 32:
            raise ValueError('Can only expand 32 bit bitstrings')
        else:
            return cls.permute(bits, cls._expand_bits)

    @staticmethod
    def permute(seq, permutation):
        """
            Runs `seq` through the given `permutation`, where `permutation` is a list of indices.

            >>> permutation = [0, 1, 3, 2]
            >>> seq = ['a', 'b', 'c', 'd']
            >>> DesCipher.permute(seq, permutation)
            ['a', 'b', 'd', 'c']
        """
        return [seq[i] for i in permutation]

    @classmethod
    def initial_permuter(cls, chunker):
        """
            Runs chunks through the Initial Permutation.

            Example:
            >>> bits = tuple(bits_of(0x8912387461283748625, 64))
            >>> chunker = DesChunker(bits, 32)
            >>> ip = DesCipher.initial_permuter(chunker)
            >>> permuted = next(ip)
            >>> permuted != (bits[:32], bits[32:])
            True
        """
        for chunk in chunker:
            # Collapse the chunk tuple into a single list
            chunk = tuple(itertools.chain.from_iterable(chunk))
            chunk = cls.permute(chunk, cls._initial_permutation)
            yield tuple(chunk[:32]), tuple(chunk[32:])

    @classmethod
    def inverse_initial_permuter(cls, chunker):
        """
            Runs chunks through the Inverse Initial Permutation.

            Example:
            >>> bits = tuple(bits_of(0x8912387461283748625, 64))
            >>> chunker = DesChunker(bits, 32)
            >>> ip = DesCipher.initial_permuter(chunker)
            >>> iip = DesCipher.inverse_initial_permuter(ip)
            >>> unpermuted = next(iip)
            >>> unpermuted == (bits[:32], bits[32:])
            True
        """
        for chunk in chunker:
            # Collapse the chunk tuple into a single list
            chunk = list(itertools.chain.from_iterable(chunk))
            chunk = cls.permute(chunk, cls._final_permutation)
            yield tuple(chunk[:32]), tuple(chunk[32:])

    @classmethod
    def s_box(cls, box, bits):
        """
            Returns the `box`th S-box value for the given `bits`

            Example:
            >>> DesCipher.s_box(4, (0, 0, 0, 1, 1, 0))
            (1, 0, 1, 1)
        """
        row = [bits[0], bits[5]]
        row = bits_to_integer(row)
        col = bits_to_integer(bits[1:5])
        s_box_value = cls._sbox[box][row][col]
        return tuple(bits_of(s_box_value, 4))

    @classmethod
    def f(cls, R, K):
        """
            The encryption function `f` in the DES algorithm

            Example:
            >>> R = tuple(bits_of(0x978612348976, 32))
            >>> K = tuple(bits_of(0x234626727892, 48))
            >>> DesCipher.f(R, K)
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1]
        """
        bits = tuple(xor_streams(cls.expand_bits(R), K))
        Bs = nslice(bits, 6)
        Ss = [cls.s_box(i, bits) for i, bits in enumerate(Bs)]
        C = list(itertools.chain.from_iterable(Ss))
        return cls.permute(C, cls._sbox_permutation)

    def feistel_round(self, L, R, i):
        """
            Runs the ith round of the Feistel System on the given chunk

            Example:
            >>> cipher = DesCipher(0x21347851283645)
            >>> bits = tuple(bits_of(0x178263487126234, 64))
            >>> cipher.feistel_round(bits[:32], bits[32:], 4)  # Run the fourth feitsel round
            ((0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1))
        """
        K = self.keys[i]
        return R, tuple(xor_streams(L, self.f(R, K)))

    def encrypt_chunk(self, chunk):
        """
            Runs the specified number of rounds on a single (L, R) chunk to encrypt it

            Example:
            >>> cipher = DesCipher(0x21347851283645)
            >>> bits = tuple(bits_of(0x178263487126234, 64))
            >>> cipher.encrypt_chunk((bits[:32], bits[32:]))
            ((0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0))
        """
        L, R = chunk
        for i in range(1, self.number_of_rounds + 1):
            L, R = self.feistel_round(L, R, i)
        return R, L

    def decrypt_chunk(self, chunk):
        """
            Runs the specified number of rounds on a single (L, R) chunk to decrypt it

            Example:
            >>> cipher = DesCipher(0x21347851283645)
            >>> chunk = ((0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1), (0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0))
            >>> cipher.decrypt_chunk(chunk)
            ((0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1), (0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0))
        """
        L, R = chunk
        # Run the feistel rounds as in encryption, but with keys going from n..1
        for i in range(self.number_of_rounds, 0, -1):
            L, R = self.feistel_round(L, R, i)
        return R, L

    def encrypt_chunks(self, chunker):
        """
            Given a chunked bitstream, yield encrypted chunk after encrypted chunk
        """
        for chunk in chunker:
            yield self.encrypt_chunk(chunk)

    def decrypt_chunks(self, chunker):
        """
            Given a chunked bitstream, yield decrypted chunk after decrypted chunk
        """
        for chunk in chunker:
            yield self.decrypt_chunk(chunk)

    def encrypt(self, message):
        """
            Encrypts the given message using the DES cipher.

            Note that every operation done is lazy, returning generators rather than lists or tuples
            to save memory.

            Example:

            >>> cipher = DesCipher(123456)
            >>> cipher.encrypt('messageX')
            'Òh*&BU¢¸'
        """
        # Pad the bitstream to be evenly divisible by 64 bit chunks. Randomly choose between 0 and 1
        bitstream = lazy_pad(TextBitstream(message), 64, pad_values=[0, 1])
        # Chunk the bitstream into 64 bit chunks --> a tuple (L, R) of 32 bit bitstrings.
        chunker = DesChunker(bitstream, 32)
        # Run each chunk through an initial permutation.
        permuter = self.initial_permuter(chunker)
        # Lazily encrypt chunk after chunk.
        encrypter = self.encrypt_chunks(permuter)
        # Unrun each chunk through the initial permutation.
        permuter = self.inverse_initial_permuter(encrypter)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(permuter)

    def decrypt(self, ciphertext):
        """
            Decrypts the given ciphertext with the DES cipher.

            Note that every operation done is lazy, returning generators rather than lists or tuples
            to save memory.

            Example:

            >>> cipher = DesCipher(123456)
            >>> cipher.decrypt('Òh*&BU¢¸')
            'messageX'
        """
        # Pad the bitstream to be evenly divisible by 64 bit chunks. Randomly choose between 0 and 1
        bitstream = lazy_pad(TextBitstream(ciphertext), 64, pad_values=[0, 1])
        # Chunk the bitstream into 64 bit chunks --> a tuple (L, R) of 32 bit bitstrings.
        chunker = DesChunker(bitstream, 32)
        # Run each chunk through an initial permutation.
        permuter = self.initial_permuter(chunker)
        # Lazily decrypt chunk after chunk.
        decrypter = self.decrypt_chunks(permuter)
        # Unrun each chunk through the initial permutation.
        permuter = self.inverse_initial_permuter(decrypter)
        # Now convert the above generator into a string and return it.
        return DesChunker.chunks_to_string(permuter)
