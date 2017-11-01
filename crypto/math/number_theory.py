"""
Various number theory functions useful for cryptography.
"""

import itertools
import math
import random
import numpy
import gmpy2
# from sympy import Matrix


def modular_matrix_inverse(matrix, modulus):
    """Computes the modular inverse of an integer matrix."""

    # If sympy import times are not an issue, the following works, and is probably more reliable
    # return Matrix(matrix).inv_mod(modulus)

    m_inv = numpy.linalg.inv(matrix)
    # Round and convert to an integer
    det = int(round(numpy.linalg.det(matrix)))
    det_inv = int(gmpy2.invert(det, modulus))
    return numpy.around(numpy.mod(det_inv * (det * m_inv), modulus))


def coprimes(num):
    """
        Yields the numbers from 1 to `num` that are coprime with `num`.

        Example:

        >>> list(coprimes(5))
        [1, 2, 3, 4]
    """
    return iter(filter(lambda x: math.gcd(x, num) == 1, range(num)))


def prime_pi(n):
    """Returns the number of primes less than n"""
    # Alternatively: return sympy.primepi(n)
    return n / math.log(n)


def random_prime(digits):
    """Generates a random large prime number with `digits` digits"""
    # TODO: There's got to be a better implementation than this...
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
               'fermat': _fermat_prime_test}

    # TODO: Speed this up by using a prime sieve for small numbers
    # Handle some easy edge cases up front
    if x == 2 or x == 3:
        return True
    if x < 2 or x % 2 == 0:
        return False

    return methods[method](x)


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


def extended_gcd(a, b):
    """Uses the Extended Euclidean Algorithm to return a triple (g, x, y) such that
       ax + by = g = gcd(a, b)"""
    prevx, x = 1, 0
    prevy, y = 0, 1

    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b

    return a, prevx, prevy


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


def factor(num, method):
    """
        Factor a number with the given method. Available methods are:

        'fermat'
        'pollard-rho'
        'pollard-p1'
        'quadratic-sieve'
        'trial-division'

        Example:
    """
    methods = {'fermat': _fermat_factor,
               'pollard-rho': _pollard_rho_factor,
               'pollard-p1': _pollard_p1_factor,
               'quadratic-sieve': _quadratic_sieve_factor,
               'trial-division': _trial_division_factors}
    return methods[method](num)


def _fermat_factor(num):
    """
        Implements Fermat's Factoring Algorithm
    """
    if num < 2:
        return []
    elif gmpy2.is_prime(num):
        return [num]
    elif num % 2 == 0:
        return [2] + _fermat_factor(num // 2)

    a = gmpy2.isqrt(num)
    b2 = gmpy2.square(a) - num

    while not gmpy2.is_square(b2):
        a += 1
        b2 = gmpy2.square(a) - num

    p = int(a + gmpy2.isqrt(b2))
    q = int(a - gmpy2.isqrt(b2))

    # Both p and q are factors of num, but neither are necessarily prime factors.
    # The case where p and q are prime is handled by the recursion base case.
    return _fermat_factor(p) + _fermat_factor(q)


def _pollard_g(x, num):
    """The function g(a) = a^2 + 1 (mod n) of the Pollard Rho algorithm"""
    return int(gmpy2.square(x) + 1) % num


def _pollard_f(x, num):
    """The function g(a) = a^2 - 1 (mod n) of the Pollard Rho algorithm"""
    return int(gmpy2.square(x) - 1) % num


def _pollard_rho_factor(num, f=_pollard_g):
    """
        Implements the Pollard Rho factorization algorithm. Passes in the function to use
        to make recursion easier.
    """

    if num < 2:
        return []
    elif num % 2 == 0:
        return [2] + _pollard_rho_factor(num // 2)
    elif gmpy2.is_prime(num):
        return [num]

    a = 2
    b = a
    d = 1

    while d == 1:
        a = f(a, num)
        b = f(f(b, num), num)
        d = math.gcd(abs(a - b), num)

    # As with Pollard P-1, this case is handled by the base case.
    # # Assert num is prime only on a reated failure
    # if d == num and f == _pollard_f:
    #     # either failure, or num is prime.
    #     return [d]
    # # Otherwise keep trying and hope the random `a` and `c` fix the issue

    # If we fail using the better function g, try the less better function f.
    if d == num and f == _pollard_g:
        return _pollard_rho_factor(num, _pollard_f)
    # Finally, recurse to find *all* factors
    return _pollard_rho_factor(d) + _pollard_rho_factor(num // d)


def _pollard_p1_factor(num, a=2):
    """
        Implements the Pollard P-1 factoring algorithm. Passes in the value of a to use
        to make recursion easier.
    """
    # Handle recursion base cases
    if num < 2:
        return []
    elif num % 2 == 0:
        return [2] + _pollard_p1_factor(num // 2)
    # I would really rather not perform a primality test each iteration.
    elif gmpy2.is_prime(num):
        return [num]

    def pollard_p1(num, bound, a):
        """Implements one iteration of the Pollard P-1 factoring algorithm."""
        for j in range(2, bound + 1):
            a = pow(a, j, num)
        d = math.gcd(a - 1, num)
        if d > 1 and d < num:
            return d
        return None

    bound = 1
    d = None
    while d is None and bound < num:
        d = pollard_p1(num, bound, a)
        bound += 1

    # We should never arrive at this case, because primality is one of our base cases.
    # if d == num:
    #     # Assert d is prime and this isn't an error.
    #     # Everything is fine. EVERYTHING IS FINE DAMMIT.
    #     return [d]

    if d is not None:
        return _pollard_p1_factor(d) + _pollard_p1_factor(num // d)
    # BUG: Occaisionally we get here and lose a factor or five.
    # FIX: Try again with a bigger a.
    return _pollard_p1_factor(num, a + 1)


def _quadratic_sieve_factor(num):
    """
        Implements the Quadratic Sieve factoring algorithm
    """
    raise NotImplementedError


def _trial_division_factors(num):
    """
        Implements naive trial division to factor a given number.
    """
    if num < 2:
        return []
    prime_factors = []
    for p in primes(int(math.sqrt(num))):
        if p * p > num:
            break
        while num % p == 0:
            prime_factors.append(p)
            num //= p
    # Num may also be a factor
    if num > 1:
        prime_factors.append(num)

    return prime_factors
