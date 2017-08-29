#!/usr/bin/python3
import sys
import numpy as np
import gmpy2 as mp
from math import gcd

ALPHABET_SIZE = 26
BLOCK_SIZE = 5


def gen_key(n, N):
    """Generate the Hill cipher matrix key"""
    # Create a random matrix from 0 to N that is nxn
    M = np.random.randint(0, N+1, (n, n))
    # The determinant of an integer matrix is an integer
    while gcd(np.linalg.det(M).astype(int), N) != 1:
        M = np.random.randint(0, N+1, (n, n))
    return M


def numberize(c):
    """Turns a character into an int"""
    # 65 = A in ascii
    return ord(c.upper()) - 65


def wordize(block):
    """Turns an int into a char"""
    return ''.join(chr(n + 65) for n in np.nditer(block, ['refs_ok']))


def vectorize(message):
    """Turns a string message into a vector of ints where a = 0, b = 1, ..."""
    return np.matrix([numberize(c) for c in message])


def nslice(seq, n, truncate=False):
    """Yield slices of seq, n elements at a time"""
    assert n > 0
    while len(seq) >= n:
        yield seq[:n]
        seq = seq[n:]
    if len(seq) and not truncate:
        yield seq


def vmap(func):
    """Creates a numpy map() function"""
    return np.vectorize(func)


def mround(m):
    """Rounds a given numpy matrix of GMP reals"""
    # vmap returns a function to call on the matrix
    return vmap(mp.rint)(m)


def main(message):
    M = gen_key(BLOCK_SIZE, ALPHABET_SIZE)
    d = int(np.linalg.det(M))
    print('d', d)
    # Compute the matrix inverse mod ALPHABET_SIZE
    # N = mround(np.linalg.inv(M) * d * mp.invert(d, ALPHABET_SIZE)).astype(int) % ALPHABET_SIZE
    N = (np.linalg.inv(M) + ALPHABET_SIZE) % ALPHABET_SIZE
    print(N)

    coded_blocks = []
    for block in nslice(message, BLOCK_SIZE):
        nums = vectorize(block)
        coded_blocks.append(np.matmul(nums, M) % ALPHABET_SIZE)
    # print('coded blocks:\n\t', coded_blocks)

    cipher = ''
    for block in coded_blocks:
        cipher += wordize(block)
    print('cipher:', cipher)

    decoded_blocks = []
    for block in coded_blocks:
        nums = np.matmul(block, N) % ALPHABET_SIZE
        decoded_blocks.append(nums.astype(int))
    # print('decoded blocks:\n\t', decoded_blocks)

    text = ''
    for block in decoded_blocks:
        text += wordize(block)
    print('text:', text)


if __name__ == '__main__':
    main('hello')
