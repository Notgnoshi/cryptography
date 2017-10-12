from crypto.ciphers import *
from crypto.random import generate_alpha
from crypto.utilities import *
import itertools
import random
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
        string = DesChunker.chunks_to_string(chunker)
        self.assertSequenceEqual(string, 'abcdef')

    def test_encrypt_1(self):
        text = 'abcdef'
        key = 0b010011001
        cipher = ToyDesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        self.assertEqual(text, plaintext)

    def test_encrypt_2(self):
        # Encrypt and decrypt a random text 10 times... That's gotta verify it works right?
        for i in range(10):
            text = generate_alpha(360)
            key = 0b010001111
            cipher = ToyDesCipher(key)
            ciphertext = cipher.encrypt(text)
            plaintext = cipher.decrypt(ciphertext)
            self.assertEqual(text, plaintext)

    def test_message_padding(self):
        # make sure the string does not end with 'x'. Add punctuation to make sure the cipher pads
        # the preprocessed message
        text = generate_alpha(random.randint(100, 800)) + 'asdf.,'
        key = 0b101010010
        cipher = ToyDesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        # Compare against the text string with the trailing punctuation removed.
        self.assertEqual(text[:-2], plaintext.rstrip('x'))


class DesCipherTest(unittest.TestCase):
    def test_expander(self):
        bits = list(bits_of(1234, 32))
        self.assertEqual(len(bits), 32)
        expanded_bits = DesCipher.expand_bits(bits)
        self.assertEqual(len(expanded_bits), 48)

    def test_initial_permutation(self):
        bits = [0] * 64
        bits[57] = 1
        bits[49] = 1
        bits[6] = 1

        expected = [0] * 64
        expected[0] = 1
        expected[1] = 1
        expected[63] = 1

        chunker = DesChunker(bits, 32)
        permuter = DesCipher.initial_permuter(chunker)
        chunk = list(itertools.chain.from_iterable(next(permuter)))
        self.assertListEqual(chunk, expected)

    def test_inverse_permutation(self):
        bits = list(bits_of(127615873723911234878, 64))
        chunker = DesChunker(bits, 32)
        IP = DesCipher.initial_permuter(chunker)
        FP = DesCipher.inverse_initial_permuter(IP)
        chunk = list(itertools.chain.from_iterable(next(FP)))
        self.assertListEqual(bits, chunk)

    def test_encrypt_1(self):
        text = 'abcdefgh'
        key = 1476123957612341
        cipher = DesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        self.assertSequenceEqual(text, plaintext)

    def test_encrypt_2(self):
        # Encrypt and decrypt a random text 10 times... That's gotta verify it works right?
        for i in range(10):
            text = generate_alpha(128)
            key = 776481980476271347
            cipher = DesCipher(key)
            ciphertext = cipher.encrypt(text)
            plaintext = cipher.decrypt(ciphertext)
            self.assertEqual(text, plaintext)

    def test_message_padding(self):
        # make sure the string does not end with 'x'. Add punctuation to make sure the cipher pads
        # the preprocessed message
        text = generate_alpha(random.randint(100, 800)) + 'asdf'
        key = 76173234526173235131
        cipher = DesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        # Compare against the text string with the trailing punctuation removed.
        self.assertEqual(text, plaintext.rstrip('x'))
