from crypto.ciphers import ToyDesCipher
from crypto.utilities import xor_streams, bits_to_integer, bits_of


class ThreeRoundDifferentialCryptanalysis(object):
    # The S-box XOR lookup table
    LOOKUP = [
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
         (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)],
        [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5), (5, 4), (6, 7), (7, 6), (8, 9),
         (9, 8), (10, 11), (11, 10), (12, 13), (13, 12), (14, 15), (15, 14)],
        [(0, 2), (1, 3), (2, 0), (3, 1), (4, 6), (5, 7), (6, 4), (7, 5), (8, 10),
         (9, 11), (10, 8), (11, 9), (12, 14), (13, 15), (14, 12), (15, 13)],
        [(0, 3), (1, 2), (2, 1), (3, 0), (4, 7), (5, 6), (6, 5), (7, 4), (8, 11),
         (9, 10), (10, 9), (11, 8), (12, 15), (13, 14), (14, 13), (15, 12)],
        [(0, 4), (1, 5), (2, 6), (3, 7), (4, 0), (5, 1), (6, 2), (7, 3), (8, 12),
         (9, 13), (10, 14), (11, 15), (12, 8), (13, 9), (14, 10), (15, 11)],
        [(0, 5), (1, 4), (2, 7), (3, 6), (4, 1), (5, 0), (6, 3), (7, 2), (8, 13),
         (9, 12), (10, 15), (11, 14), (12, 9), (13, 8), (14, 11), (15, 10)],
        [(0, 6), (1, 7), (2, 4), (3, 5), (4, 2), (5, 3), (6, 0), (7, 1), (8, 14),
         (9, 15), (10, 12), (11, 13), (12, 10), (13, 11), (14, 8), (15, 9)],
        [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0), (8, 15),
         (9, 14), (10, 13), (11, 12), (12, 11), (13, 10), (14, 9), (15, 8)],
        [(0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15),
         (8, 0), (9, 1), (10, 2), (11, 3), (12, 4), (13, 5), (14, 6), (15, 7)],
        [(0, 9), (1, 8), (2, 11), (3, 10), (4, 13), (5, 12), (6, 15), (7, 14),
         (8, 1), (9, 0), (10, 3), (11, 2), (12, 5), (13, 4), (14, 7), (15, 6)],
        [(0, 10), (1, 11), (2, 8), (3, 9), (4, 14), (5, 15), (6, 12), (7, 13),
         (8, 2), (9, 3), (10, 0), (11, 1), (12, 6), (13, 7), (14, 4), (15, 5)],
        [(0, 11), (1, 10), (2, 9), (3, 8), (4, 15), (5, 14), (6, 13), (7, 12),
         (8, 3), (9, 2), (10, 1), (11, 0), (12, 7), (13, 6), (14, 5), (15, 4)],
        [(0, 12), (1, 13), (2, 14), (3, 15), (4, 8), (5, 9), (6, 10), (7, 11),
         (8, 4), (9, 5), (10, 6), (11, 7), (12, 0), (13, 1), (14, 2), (15, 3)],
        [(0, 13), (1, 12), (2, 15), (3, 14), (4, 9), (5, 8), (6, 11), (7, 10),
         (8, 5), (9, 4), (10, 7), (11, 6), (12, 1), (13, 0), (14, 3), (15, 2)],
        [(0, 14), (1, 15), (2, 12), (3, 13), (4, 10), (5, 11), (6, 8), (7, 9),
         (8, 6), (9, 7), (10, 4), (11, 5), (12, 2), (13, 3), (14, 0), (15, 1)],
        [(0, 15), (1, 14), (2, 13), (3, 12), (4, 11), (5, 10), (6, 9), (7, 8),
         (8, 7), (9, 6), (10, 5), (11, 4), (12, 3), (13, 2), (14, 1), (15, 0)]
    ]

    def __init__(self):
        raise NotImplementedError


def analyze(cipher, input1, input2):
    """
        Analyze the differences in the outputs with respect to the given inputs, when ran through
        the given cipher object.
    """
    L4, R4 = cipher.encrypt_chunk(input1, rounds=[2, 3, 4])
    L4S, R4S = cipher.encrypt_chunk(input2, rounds=[2, 3, 4])

    E4 = cipher.expand_bits(L4)
    E4S = cipher.expand_bits(L4S)

    # Ths S-boxe's input XOR, 4-bits each
    difference = tuple(xor_streams(E4, E4S))
    S1IX = bits_to_integer(difference[:4])
    S2IX = bits_to_integer(difference[4:])

    # The S-box output XOR, 6-bits
    SOX = tuple(xor_streams(xor_streams(input1[0], input2[0]), xor_streams(R4, R4S)))

    poss1 = set()
    poss2 = set()
    # Iterate over all pairs a four bit numbers to compare the XOR of the S-box outputs
    for left, right in ThreeRoundDifferentialCryptanalysis.LOOKUP[S1IX]:
        left_bits = tuple(bits_of(left, 4))
        right_bits = tuple(bits_of(right, 4))
        if tuple(xor_streams(cipher.S1(left_bits), cipher.S1(right_bits))) == SOX[:3]:
            poss1.add(left_bits)

    for left, right in ThreeRoundDifferentialCryptanalysis.LOOKUP[S2IX]:
        left_bits = tuple(bits_of(left, 4))
        right_bits = tuple(bits_of(right, 4))
        if tuple(xor_streams(cipher.S2(left_bits), cipher.S2(right_bits))) == SOX[3:]:
            poss2.add(left_bits)

    return poss1, poss2


# key = 0b001001101
# cipher = ToyDesCipher(key, 3)
# L1, R1 = (0, 0, 0, 1, 1, 1), (0, 1, 1, 0, 1, 1)
# L1S, R1S = (1, 0, 1, 1, 1, 0), (0, 1, 1, 0, 1, 1)
# possibilities1, possibilities2 = analyze(
#     cipher, (L1, R1), (L1S, R1S))
#
# # Correct
# print('1: first four:', possibilities1)
# # Correct
# print('1: last four:', possibilities2)
#
# L1, R1 = (0, 1, 0, 1, 1, 1), (0, 1, 1, 0, 1, 1)
# L1S, R1S = (1, 0, 1, 1, 1, 0), (0, 1, 1, 0, 1, 1)
# possibilities3, possibilities4 = analyze(
#     cipher, (L1, R1), (L1S, R1S))
#
# # Correct
# print('2: first four:', possibilities3)
# # Correct
# print('2: last four:', possibilities4)
