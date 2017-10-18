from crypto.utilities import nslice
import itertools
import string


def chunker(text, chunk_size=5, fill_value=None):
    """
        Returns chunk after chunk of `text` with chunk size `chunk_size`
        and fill character `fill_value`. Equivalent to using ''.join() on
        the output of crypto.utilities.nslice.
    """
    for chunk in nslice(text, chunk_size, fill_value=fill_value):
        yield ''.join(chunk)
