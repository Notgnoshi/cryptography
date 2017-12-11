from crypto.attacks import *
from crypto.classical import *
from crypto.math import coprimes
from crypto.utilities import rotate
from crypto.samples import *
import unittest


class AffineAttackTest(unittest.TestCase):
    def test_affine_naive(self):
        attack = AffineAttack(affine_well_behaved_ciphertext)
        decrypted = attack.naive_frequency()
        self.assertSequenceEqual(decrypted, well_behaved_plaintext)

    def test_all_keys_naive(self):
        # Does a naive attack work on all combinations of a and b for this plaintext?
        for a in coprimes(26):
            for b in range(26):
                cipher = AffineCipher(a, b)
                ciphertext = cipher.encrypt(well_behaved_plaintext)
                attack = AffineAttack(ciphertext)
                decrypted = attack.naive_frequency()
                self.assertSequenceEqual(decrypted, well_behaved_plaintext)

    def test_brute_force(self):
        attack = AffineAttack(affine_well_behaved_ciphertext)
        candidates = []
        for plaintext, a, b in attack.brute_force():
            if plaintext.startswith('who'):
                candidates.append((a, b))

        self.assertListEqual(candidates, [(9, 18)])


class VigenereAttackTest(unittest.TestCase):
    def test_vigenere_coincidences(self):
        coincidences = []
        # The book says [14, 14, 16, 14, 24, 12]
        actual_coincidences = [14, 14, 16, 15, 25, 12]
        for r in range(1, 7):
            coincidences.append(VigenereAttack.coincidences(
                vigenere_ciphertext, rotate(vigenere_ciphertext, -r)))

        self.assertListEqual(coincidences, actual_coincidences)

    def test_vigenere_key_length(self):
        attack = VigenereAttack(vigenere_ciphertext)
        self.assertEqual(attack.probable_key_length(), 5)

    def test_book_vigenere_attack(self):
        attack = VigenereAttack(vigenere_ciphertext)
        key = attack.probable_key()
        self.assertEqual(key, 'codes')
        cipher = VigenereCipher(key)
        self.assertEqual(cipher.decrypt(vigenere_ciphertext), vigenere_plaintext)

    def test_weak_key(self):
        key = 'somekey'
        cipher = VigenereCipher(key)
        ciphertext = cipher.encrypt(well_behaved_message)
        attack = VigenereAttack(ciphertext)
        self.assertEqual(attack.probable_key_length(), len(key))
        self.assertEqual(attack.probable_key(), key)

    def test_stronger_key(self):
        key = 'thisisakey'
        cipher = VigenereCipher(key)
        ciphertext = cipher.encrypt(well_behaved_message)
        attack = VigenereAttack(ciphertext)
        self.assertEqual(attack.probable_key_length(), len(key))
        self.assertEqual(attack.probable_key(), key)
