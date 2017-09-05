#!/usr/bin/python3
from affine import AffineCipher
import math
import random


def main():
    message = 'thisisatest'
    # Generate lists of numbers relatively prime with 26.
    lesser_nums = filter(lambda x: math.gcd(x, 26) == 1, range(0, 27))
    greater_nums = filter(lambda x: math.gcd(x, 26) == 1, range(26, 26 * 2))

    # Pairwise iterate over lesser and greater numbers.
    for l, g in zip(lesser_nums, greater_nums):
        shift = random.randrange(0, 27)
        lesser = AffineCipher(l, shift)
        greater = AffineCipher(g, shift)

        l_cipher = lesser.encrypt(message)
        g_cipher = greater.encrypt(message)
        print('lesser ({}): {}'.format(l, l_cipher))
        print('greater ({}): {}'.format(g, g_cipher))


if __name__ == '__main__':
    main()
