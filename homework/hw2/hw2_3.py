#!/usr/bin/python3


def roots_mod(square, modulus):
    """Solves the equation: x^2 \equiv `square` (mod `modulus`)"""
    for i in range(1, modulus + 1):
        if (i ** 2) % modulus == square:
            yield i


if __name__ == '__main__':
    print(list(roots_mod(133, 143)))
    print(list(roots_mod(77, 143)))
