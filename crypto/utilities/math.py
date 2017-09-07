import gmpy2
import math
import numpy


class Math(object):
    """A utility class for common mathematical operations"""

    def modular_matrix_inverse(matrix, modulus):
        """Computes the modular inverse of an integer matrix given by the formula
           M^{-1} \pmod{n} = \det(A)^{-1} \mod{n} \cdot (\det(A) A^{-1}) \pmod{n}"""

        # If sympy import times are not an issue, the following works, and is probably more reliable
        # from sympy import Matrix
        # return Matrix(matrix).inv_mod(modulus)

        # Make sure the input is a numpy integer matrix
        m = numpy.matrix(matrix, dtype=int)
        m_inv = numpy.linalg.inv(m)
        # Round and convert to an integer
        det = int(round(numpy.linalg.det(m)))
        det_inv = gmpy2.invert(det, modulus)
        return numpy.mod(det_inv * (det * m_inv), modulus).astype(int)
