from crypto.classical import VigenereCipher
from crypto.random import generate_alpha
import random
import unittest


class VigenereCipherTest(unittest.TestCase):
    def test_vigenere_encrypt(self):
        key = 'vector'
        plaintext = 'hereishowitworks'
        expected = 'citxwjcsybhnjvml'
        vigenere = VigenereCipher(key)
        ciphertext = vigenere.encrypt(plaintext)
        self.assertSequenceEqual(ciphertext, expected)

    def test_vigenere_decrypt(self):
        key = 'vector'
        expected = 'hereishowitworks'
        ciphertext = 'citxwjcsybhnjvml'
        vigenere = VigenereCipher(key)
        plaintext = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, expected)

    def test_vigenere_large(self):
        key = 'hereissomerandomkeythaticouldntthinkof'
        vigenere = VigenereCipher(key)
        plaintext = generate_alpha(random.randint(1000, 10000)).lower()
        ciphertext = vigenere.encrypt(plaintext)
        message = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, message)

    def test_vigenere_larger(self):
        key = generate_alpha(random.randint(100, 1000)).lower()
        vigenere = VigenereCipher(key)
        plaintext = generate_alpha(random.randint(10000, 100000)).lower()
        ciphertext = vigenere.encrypt(plaintext)
        message = vigenere.decrypt(ciphertext)
        self.assertSequenceEqual(plaintext, message)
