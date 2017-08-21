#!/usr/bin/python3
from collections import Counter
from operator import itemgetter
import sys


def counter(text):
    with open(text, 'r') as f:
        string = ''.join(line.strip() for line in f)
        return Counter(''.join(c.lower() for c in string if c.isalpha()))


def main(texts):
    for text in texts:
        count = counter(text)
        print(80*'=')
        print('file:', text)
        for key, value in sorted(count.items(), key=itemgetter(1), reverse=True):
            print('   ', key, value)
        print(80*'=')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <text>')
    main(sys.argv[1:])
