#!/usr/bin/python3
import sys
import gmpy2
sys.path.append('../../')
from crypto.utilities import char_mapping

ciphertext = [(949,   2750),  (8513,  28089), (5513,  8421),
              (4769,  4261),  (18352, 12856), (17914, 28599),
              (25231, 9196),  (3809,  5997),  (1477,  19626),
              (19108, 22326), (24966, 631),   (3494,  5974),
              (10256, 30308), (29093, 15082), (4223,  25106),
              (3595,  18546), (11325, 3588),  (5632,  4912),
              (18067, 13223), (21530, 3138),  (30949, 16065),
              (29784, 7987),  (6385,  5955),  (27338, 10405),
              (31715, 15969), (15815, 28055), (10462, 13371),
              (4852,  28393), (1331,  30788), (18117, 28680),
              (2472,  11786), (27548, 22909), (21980, 28433),
              (2154,  3440),  (21504, 22036), (13651, 18061),
              (10676, 26545), (30974, 23306), (14689, 8359)]
message = []

p, alpha, beta = 31847, 5, 18074
a = 7899


def decrypt(r, t):
    """Decrypt a ciphertext pair using the private encryption exponent a"""
    return t * gmpy2.invert(r ** a, p) % p


def translate(num):
    """Convert a number in Z_p to a triple of characters"""
    triple = []
    while num:
        triple.append(num % 26)
        num //= 26
    return ''.join(map(char_mapping, triple[::-1]))


print(''.join(translate(decrypt(r, t)) for r, t in ciphertext))
