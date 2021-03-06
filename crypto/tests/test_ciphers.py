from crypto.ciphers import *
from crypto.random import generate_alpha
from crypto.utilities import *
from crypto.samples import *
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
        text = generate_alpha(13)
        key = 0b101010010
        cipher = ToyDesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        # Compare against the text string with the trailing punctuation removed.
        self.assertEqual(text, plaintext[:-2])


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
        text = generate_alpha(17)
        key = 76173234526173235131
        cipher = DesCipher(key)
        ciphertext = cipher.encrypt(text)
        plaintext = cipher.decrypt(ciphertext)
        # Compare against the text string with the trailing padding
        self.assertEqual(text, plaintext[:-7])


class RsaCipherTest(unittest.TestCase):
    def test_small_message(self):
        # Example taken from the book
        # private
        p = 885320963
        q = 238855417
        d = 116402471153538991

        # public
        e = 9007
        n = p * q

        cipher = BaseRsaCipher(n, e, d)
        ciphertext = cipher.encrypt_number(cipher.str2num('cat'))
        plaintext = cipher.num2str(cipher.decrypt_number(ciphertext))
        self.assertEqual(plaintext, 'cat')

    def test_large_message(self):
        # private
        p = 885320963
        q = 238855417
        d = 116402471153538991

        # public
        e = 9007
        n = p * q

        cipher = RsaCipher(n, e, d)
        # Pad the plaintext beforehand so it isn't padded with random text
        ciphertext = cipher.encrypt(well_behaved_plaintext + 'zz')
        plaintext = cipher.decrypt(ciphertext)
        self.assertEqual(plaintext, well_behaved_plaintext + 'zz')

    def test_rsa_keygen(self):
        bits = 64
        keygen = RsaKeyGenerator(bits)
        n, e = keygen.public_key
        d = keygen.private_key
        self.assertEqual(e * d % keygen.limit, 1)
        self.assertGreaterEqual(n.bit_length(), bits)

        # Takes about 0.5 seconds to generate
        bits = 256
        keygen = RsaKeyGenerator(bits)
        n, e = keygen.public_key
        d = keygen.private_key
        self.assertEqual(e * d % keygen.limit, 1)
        self.assertGreaterEqual(n.bit_length(), bits)

        # Takes about 0.8 seconds to generate
        # bits = 512
        # keygen = RsaKeyGenerator(bits)
        # n, e = keygen.public_key
        # d = keygen.private_key
        # self.assertEqual(e * d % keygen.limit, 1)
        # self.assertGreaterEqual(n.bit_length(), bits)

        # Takes about 9 seconds to generate
        # bits = 1024
        # keygen = RsaKeyGenerator(bits)
        # n, e = keygen.public_key
        # d = keygen.private_key
        # self.assertEqual(e * d % keygen.limit, 1)
        # self.assertGreaterEqual(n.bit_length(), bits)

    def test_rsa_random_key(self):
        bits = 64
        keygen = RsaKeyGenerator(bits)
        n, e = keygen.public_key
        d = keygen.private_key
        cipher = RsaCipher(n, e, d)
        ciphertext = cipher.encrypt(well_behaved_plaintext)
        plaintext = cipher.decrypt(ciphertext)
        # The cipher pads the text...
        self.assertEqual(well_behaved_plaintext, plaintext[:769])
