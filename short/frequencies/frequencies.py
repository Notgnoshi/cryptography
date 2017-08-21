#!/usr/bin/python3
from collections import Counter
from operator import itemgetter
import sys

if sys.version_info[0] < 3:
    raise EnvironmentError("Python 3+ is required.")


def alphabet(text):
    """Return only English alphabetic characters of given text"""
    with open(text, 'r') as f:
        # Project Gutenberg encodes its documents with utf-8, and some books use diacritic marks
        # Avoid encoding as ascii and then decoding back into text if unicode alphabetic characters
        # are acceptable.
        s = ''.join(line.strip() for line in f).encode('ascii', errors='ignore').decode().upper()
        return filter(str.isalpha, s)


def main(texts):
    """Print the letter frequency table for the given files."""
    for text in texts:
        count = Counter(alphabet(text))
        print(80*'=')
        print('file:', text)
        print(80*'=')
        print('\tsymbol:\tcount:\tfraction:')
        total = sum(count.values())
        for key, value in sorted(count.items(), key=itemgetter(1), reverse=True):
            print('\t{}\t{}\t{:.3f}'.format(key, value, value / total))


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print(main.__doc__)
        print('Usage: {} <text 1> <text 2> ...')
    elif len(sys.argv) < 2:
        print('Usage: {} <text 1> <text 2> ...')
    else:
        main(sys.argv[1:])
