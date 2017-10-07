import string

ALPHABET = frozenset(string.ascii_lowercase)


def preprocessor(text, ascii=True):
    """
        Preprocess text. Converts to lowercase and filters non-alphabetic characters.
        Defaults to defining alphabetic characters as ascii-alphabetic
    """
    if ascii:
        return filter(ALPHABET.__contains__, text.lower())
    else:
        return filter(str.isalpha, text.lower())
