import itertools
import random
import gmpy2


# TODO: convert this to take in a given number of bits...
# TODO: There's got to be a better implementation than this...
def random_prime(digits):
    """Generates a random large prime number with `digits` digits"""
    # Generate a random number with n digits
    num = random.randint(10**(digits - 1) + 1, 10**digits)
    # Find the next prime after the number - will *probably* have n digits.
    return gmpy2.next_prime(num)


def is_prime(x, method='miller-rabin'):
    """
        Returns True if x is prime, False otherwise. Uses the given primality test, which defaults
        to Miller Rabin. The given method may be one of the following: 'fermat' or 'miller-rabin'

        Example:

        >>> is_prime(11)
        True
        >>> is_prime(11, method='miller-rabin')  # Equivalent to the above
        True
        >>> is_prime(11, method='fermat')
        True
    """

    methods = {'miller-rabin': _miller_rabin_prime_test,
               'fermat': _fermat_prime_test,
               'solovay-strassen': _solovay_strassen_prime_test,
              }

    # TODO: Speed this up by using a prime sieve for small numbers
    # Handle some easy edge cases up front
    if x == 2 or x == 3:
        return True
    if x < 2 or x % 2 == 0:
        return False

    return methods[method](x)


# TODO: use sieve of sundaram or wheel factorization?
def _primes():
    """An infinite prime generator for internal use."""
    start = 1
    while True:
        # Convert from mpz() to Python int
        start = int(gmpy2.next_prime(start))
        yield start


def primes(limit=None):
    """
        A generator that yields the first `limit` primes. Defaults to infinite primes.
        Uses gmpy2.next_prime() to generate prime after prime.

        Example:

        >>> p = primes(10)
        >>> list(p)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit is None:
        return _primes()
    return itertools.islice(_primes(), limit)


def _miller_rabin_decompose(n):
    """
        Decomposes the given even integer into some power of two and some remainder
    """
    power = 0
    # Repeatedly divide by two until the number disappears
    while not n % 2:
        # Force Python 3 to use integer division
        n = n // 2
        power += 1
    return power, n


def _miller_rabin_is_witness(potential_witness, n, power, remainder):
    """
        Returns True if the given potential_witness is a Miller Rabin witness, and False otherwise.
        False implies that n is probably prime, and True implies the n is definitely not prime.
    """
    # a^q (mod n)
    potential_witness = pow(potential_witness, remainder, n)
    # Implies n is prime, so potential_witness is not a witness
    if potential_witness == 1 or potential_witness == n - 1:
        return False

    # For each a^{2^k * q}
    for _ in range(power):
        potential_witness = pow(potential_witness, 2, n)
        if potential_witness == 1 or potential_witness == n - 1:
            return False
    return True


def _miller_rabin_prime_test(x, attempts=25):
    """
        Implements the Miller Rabin primality test
    """
    # Find 2^s as the largest power of two that divides x-1
    power, remainder = _miller_rabin_decompose(x - 1)
    for _ in range(attempts):
        # Generate a random potential witness
        potential_witness = random.randint(2, x - 2)
        if _miller_rabin_is_witness(potential_witness, x, power, remainder):
            # If we find a witness, the given number is definitely not prime
            return False
    # If we make it through the witness testing, the number is probably prime
    return True


def _fermat_prime_test(x, attempts=25):
    """
        Implements the Fermat primality (compositeness) test
    """
    for _ in range(attempts):
        a = random.randint(1, x - 1)
        if pow(a, x - 1, x) != 1:
            return False
    return True


def _solovay_strassen_prime_test(x):
    """
        Implements the Solovay-Strassen primality test
    """
    raise NotImplementedError
