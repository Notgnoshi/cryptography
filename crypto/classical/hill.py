from crypto.utilities import Math
import gmpy2
import math
import numpy


class HillCipher(object):
    @classmethod
    def generate_key(cls, block_size, alphabet_size):
        """Generate the Hill cipher matrix key"""
        # Create a random matrix from 0 to N that is nxn
        M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        # The determinant of an integer matrix is an integer
        while math.gcd(int(round(numpy.linalg.det(M))), alphabet_size) != 1:
            M = numpy.random.randint(0, alphabet_size + 1, (block_size, block_size))
        return M
