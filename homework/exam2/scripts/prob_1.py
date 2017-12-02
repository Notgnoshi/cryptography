#!/usr/bin/python3
from math import sqrt
import sys
sys.path.append('../../')
from crypto.random import random_prime


def quadratic(a, b, c):
    d = b**2 - 4 * a * c
    return (-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)


p = random_prime(16)
q = random_prime(16)

n = p * q
phi = (p - 1) * (q - 1)

a = 1
b = -(n + 1 - phi)
c = n

print(p, q)
print(quadratic(a, b, c))
