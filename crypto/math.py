import numpy
import math


class Math(object):
    """A utility class for common mathematical operations"""

    def modular_inverse(matrix, modulus):
        """Computes the modular inverse of a matrix"""
        a = round(numpy.linalg.inv(matrix))
