from crypto import Math
import numpy as np
import unittest


class MathTest(unittest.TestCase):
    def test_modular_matrix_inverse(self):
        m = np.matrix([[7, 14], [20, 19]])
        m_inv = np.matrix([[5, 10], [18, 21]], dtype=int)
        self.assertSequenceEqual(Math.modular_matrix_inverse(m, 26).tolist(), m_inv.tolist())
