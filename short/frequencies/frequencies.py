#!/usr/bin/python3
import sys
sys.path.append('../../')
from crypto import SymbolFrequencies


def main(texts):
    """Print the letter frequency table for the given files."""
    for text in texts:
        with open(text, 'r') as f:
            count = SymbolFrequencies(''.join(f).upper())
            print(80 * '=')
            print('file:', text)
            print(80 * '=')
            print(count)


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
        print(main.__doc__)
        print('Usage: {} <text 1> <text 2> ...'.format(sys.argv[0]))
    else:
        main(sys.argv[1:])
