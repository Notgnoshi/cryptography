#!/usr/bin/python3
import sys
import numpy
from sympy.core.numbers import mod_inverse
from math import gcd

ALPHABET_SIZE = 26
BLOCK_SIZE = 3


def gen_key(n=BLOCK_SIZE, N=ALPHABET_SIZE):
    M = numpy.random.randint(0, ALPHABET_SIZE+1, (n, n))
    while gcd(int(numpy.linalg.det(M)), ALPHABET_SIZE) != 1:
        M = numpy.random.randint(0, ALPHABET_SIZE+1, (n, n))
    return M


def numberize(c):
    """Turns a character into an int"""
    # 65 = A in ascii
    return ord(c.upper()) - 65


def wordize(n):
    """Turns an int into a char"""
    return chr(n)


def vectorize(message):
    """Turns a string message into a vector of ints where a = 0, b = 1, ..."""
    return numpy.array([numberize(c) for c in message])


def nslice(s, n, truncate=False):
    assert n > 0
    while len(s) >= n:
        yield s[:n]
        s = s[n:]
    if len(s) and not truncate:
        yield s


def main(message):
    M = numpy.array([[1, 2, 3], [4, 5, 6], [11, 9, 8]])
    print(M)
    d = numpy.linalg.det(M)
    print(d)
    M_inv = numpy.linalg.inv(M) * (1/mod_inverse(d, ALPHABET_SIZE)) * d
    print(M_inv % ALPHABET_SIZE)

    coded_blocks = []
    for block in nslice(message, BLOCK_SIZE):
        nums = vectorize(block)
        coded_blocks.append((nums * M) % 26)

    print(coded_blocks)

    decoded_blocks = []
    for block in coded_blocks:
        nums = block * M_inv
        decoded_blocks.append(nums)

    # print(decoded_blocks)

    text = ''
    for block in decoded_blocks:
        text += ''.join(wordize(c) for c in block)
    print(text)


if __name__ == '__main__':
    main('hellox')
