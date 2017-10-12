from crypto.ciphers import *
from crypto.random import generate_alpha
from crypto.utilities import *
import unittest


class ToyDesCipherTest(unittest.TestCase):
    def test_expander(self):
        bits = [1, 0, 0, 1, 1, 0]
        expected = [1, 0, 1, 0, 1, 0, 1, 0]
        actual = ToyDesCipher.expand_bits(bits)
        self.assertListEqual(actual, expected)

    def test_chunker_1(self):
        bits = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        expected_L1 = (1, 1, 1, 1, 1, 1)
        expected_R1 = (0, 0, 0, 0, 0, 0)
        expected_L2 = (1, 1, 1, 0, 0, 0)
        expected_R2 = (0, 0, 0, 1, 1, 1)

        chunker = DesChunker(bits, 6)

        L, R = next(chunker)
        self.assertTupleEqual(L, expected_L1)
        self.assertTupleEqual(R, expected_R1)

        L, R = next(chunker)
        self.assertTupleEqual(L, expected_L2)
        self.assertTupleEqual(R, expected_R2)

    def test_chunker_2(self):
        bitstream = TextBitstream('abcdef')
        # A list of tuples (L, R)
        chunks = [((1, 0, 0, 0, 0, 1), (1, 0, 0, 1, 0, 0)),
                  ((0, 1, 1, 0, 1, 1), (0, 0, 0, 1, 1, 0)),
                  ((0, 0, 1, 0, 0, 1), (1, 0, 1, 0, 1, 0)),
                  ((0, 1, 1, 0, 0, 1), (1, 0, 0, 1, 1, 0)), ]

        chunker = DesChunker(bitstream, 6)
        for i, chunk in enumerate(chunker):
            self.assertTupleEqual(chunk, chunks[i])

    def test_chunker_3(self):
        bitstream = TextBitstream('abcdef')
        chunker = DesChunker(bitstream, 6)
        string = ToyDesCipher.chunks_to_string(chunker)
        self.assertSequenceEqual(string, 'abcdef')

    def test_encrypt_1(self):
        text = 'abcdef'
        key = [0, 1, 0, 0, 1, 1, 0, 0, 1]
        cipher = ToyDesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        self.assertEqual(text, plaintext)

    def test_encrypt_2(self):
        # Encrypt and decrypt a random text 10 times... That's gotta verify it works right?
        for i in range(10):
            text = generate_alpha(360)
            key = [0, 1, 0, 0, 0, 1, 1, 1, 1]
            cipher = ToyDesCipher(key)
            ciphertext = cipher.encrypt(text)
            plaintext = cipher.decrypt(ciphertext)
            self.assertEqual(text, plaintext)
