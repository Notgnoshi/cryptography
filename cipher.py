#!/usr/bin/python3
import argparse
import sys
from crypto.classical import AffineCipher, HillCipher, LfsrCipher, VigenereCipher
from crypto.ciphers import DesCipher, ToyDesCipher


SUPPORTED_CIPHERS = {'des': DesCipher,
                     'toy_des': ToyDesCipher,
                     'affine': AffineCipher,
                     'hill': HillCipher,
                     'lfsr': LfsrCipher,
                     'vigenere': VigenereCipher,
                    }


def parse_args():
    VERSION = 'alpha'
    DESCRIPTION = 'Encrypts and Decrypts files from the commandline'

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    action_group = parser.add_mutually_exclusive_group()
    verbosity_group = parser.add_mutually_exclusive_group()

    # No program is complete without a version flag
    parser.add_argument('-V', '--version',
                        action='version',
                        version=VERSION)

    # Verbosity settings
    verbosity_group.add_argument('-v', '--verbose',
                                 action='store_true',
                                 default=False,
                                 help='Increase output verbosity')
    verbosity_group.add_argument('-q', '--quiet',
                                 action='store_true',
                                 default=False,
                                 help='Suppress any output.')

    # Action settings
    action_group.add_argument('-e', '--encrypt',
                              action='store_true',
                              default=True,
                              help='Set tool to encrypt the given file')
    action_group.add_argument('-d', '--decrypt',
                              action='store_true',
                              default=False,
                              help='Set tool to decrypt the given file')

    # Allow for piping to/from stdin/stdout
    parser.add_argument('--pipe-mode',
                        action='store_true',
                        default=False,
                        help='Output encrypted/decrypted contents to stdout.')

    # Pick the cipher to use
    parser.add_argument('cipher',
                        choices=SUPPORTED_CIPHERS.keys(),
                        help='The cipher to use for encryption/decryption')

    # The cipher Key, given as a file
    parser.add_argument('key',
                        type=argparse.FileType('r'),
                        # default=sys.stdin,
                        # nargs='?',
                        help='The key to use for encryption/decryption')

    # The file to encrypt, given as a file or stdin
    parser.add_argument('file',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        nargs='?',
                        help='The file to encrypt/decrypt')

    return parser.parse_args()


def encrypt(in_file, out_file, cipher):
    """A function to encrypt a file with the given cipher"""
    out_file.write(cipher.encrypt(in_file))


def decrypt(in_file, out_file, cipher):
    """A function to decrypt a file with the given cipher"""
    out_file.write(cipher.decrypt(in_file))


def main():
    args = parse_args()
    # TODO: need to instantiate the cipher with the key
    #       but this will be different depending on the cipher...
    cipher = SUPPORTED_CIPHERS[args.cipher](args.key)

    if args.pipe_mode:
        out_file = sys.stdout
    else:
        # TODO: if .dec or .enc is already present, remove.
        if args.encrypt:
            out_file = args.file + '.enc'
        else:
            out_file = args.file + '.dec'

    if args.encrypt:
        encrypt(args.file, out_file, cipher)
    else:
        decrypt(args.file, out_file, cipher)


if __name__ == '__main__':
    main()
