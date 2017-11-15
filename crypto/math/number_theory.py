"""
Various number theory functions useful for cryptography.
"""
from collections import Counter
import itertools
import math
import platform
import random
import subprocess
import numpy
import gmpy2
from crypto.utilities import product


"""
Misc Number Theory
"""


def modular_matrix_inverse(matrix, modulus):
    """Computes the modular inverse of an integer matrix."""

    # If sympy import times are not an issue, the following works, and is probably more reliable
    # from sympy import Matrix
    # return Matrix(matrix).inv_mod(modulus)

    m_inv = numpy.linalg.inv(matrix)
    # Round and convert to an integer
    det = int(round(numpy.linalg.det(matrix)))
    det_inv = int(gmpy2.invert(det, modulus))
    return numpy.around(numpy.mod(det_inv * (det * m_inv), modulus))


def mod_inverse(num, modulus):
    """
        Computes the modular multiplicative inverse of `num` mod `modulus` using the Extended
        Euclidean Algorithm.

        Example:

        >>> mod_inverse(3, 11)
        4
        >>> mod_inverse(10, 17)
        12
    """
    _, x, _ = xgcd(num, modulus)
    return x % modulus


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
    return itertools.islice(_primes(), limit)


# TODO: convert this to take in a given number of bits...
# TODO: There's got to be a better implementation than this...
def random_prime(digits):
    """Generates a random prime number with `digits` digits"""
    # Generate a random number with n digits
    num = random.randint(10**(digits - 1) + 1, 10**digits)
    # Find the next prime after the number - will *probably* have n digits.
    return int(gmpy2.next_prime(num))


def legendre(a, p):
    """
        The Legendre Symbol of `a` mod `p`.

        Example:

        >>> legendre(6, 11)
        -1
        >>> legendre(7, 11)
        -1
        >>> legendre(42, 11)
        1
    """
    if a == 0:
        return 0
    elif pow(a, (p - 1) // 2, p) == p - 1:
        return -1
    return 1


def jacobi(a, n):
    """
        The Jacobi Symbol of `a` mod `n`

        Example:

        >>> jacobi(4567, 12345)
        -1
        >>> jacobi(107, 137)
        1
    """
    factors = Counter(factor(n, 'pollard-p1'))
    return product(legendre(a, f) ** b for f, b in factors.items())


def sqrt_mod(a, p):
    """
        Computes the square root of `a` mod `p`. That is, it solves the congruence of the form:
            x^2 = a (mod p)
        Returns None if no solution was found. Note that `p` must be an odd prime.

        Example:
    """
    if legendre(a, p) != 1:
        return None
    elif a == 0:
        return None
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) / 4, p)

    # Factor all powers of 2 out of p-1
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some n who is a square mod p
    n = 2
    while legendre(n, p) != -1:
        n += 1

    # The Tonelli-Shanks algorithm.
    # estimate is an iterative approximation
    # fudge is a 'fudge' factor with estimate^2 = a * fudge (mod p)
    estimate = pow(a, (s + 1) // 2, p)
    fudge = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        f = fudge
        m = 0
        for m in range(r):
            if f == 1:
                break
            f = pow(f, 2, p)

        if m == 0:
            return estimate

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        estimate = (estimate * gs) % p
        fudge = (fudge * g) % p
        r = m


def gcd(a, b):
    """
        Implements the Euclidea Algorithm to find the GCD of `a` and `b`.

        Example:

        >>> gcd(23, 65)
        1
        >>> gcd(5, 65)
        5
    """
    g, _, _ = xgcd(a, b)
    return g


def xgcd(a, b):
    """
        Uses the Extended Euclidean Algorithm to return a triple (g, x, y) such that
        ax + by = g = gcd(a, b)

        Example:

        >>> xgcd(7, 65)
        (1, 28, -3)
        >>> assert 28 * 7 - 3 * 65 == 1

    """
    prevx, x = 1, 0
    prevy, y = 0, 1

    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b

    return a, prevx, prevy


def primitive_roots(n):
    """
        Yields the primitive roots of the composite number `n`

        Example:

        >>> list(primitive_roots(11))
        [2, 6, 7, 8]
    """
    # Wikipedia defines coprime for a composite number using the coprimes of that number,
    # while our textbook uses all numbers up to a prime `p`. For generality prefer composite n.
    cop = set(coprimes(n))
    for a in cop:
        if set(pow(a, x, n) for x in range(1, n)) == cop:
            yield a


def is_primitive_root(a, p):
    """
        Determine if `a` is a primitive root mod a prime number `p`

        Example:

        >>> is_primitive_root(3, 13)
        False
        >>> is_primitive_root(2, 13)
        True
    """
    return set(pow(a, x, p) for x in range(1, p)) == set(range(1, p))


def wheel_factorization():
    """
        Implements Wheel Factorization to yield primes

        Example:
    """
    raise NotImplementedError


def sundaram_sieve():
    """
        Implements the Sieve of Sundaram to yield primes

        Example:
    """
    raise NotImplementedError


def eratosthenes_sieve(limit):
    """
        Implements the Sieve of Eratosthenes to yield primes less than `limit`

        Example:
    """
    # Use numpy for speed and memory
    sieve = numpy.ones(limit // 2, dtype=numpy.bool)
    for i in range(3, int(math.sqrt(limit)) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False]
    # This fails to classify 2 as prime, so prepend [2]
    return numpy.append([2], (2 * numpy.nonzero(sieve)[0][1::] + 1)).tolist()


"""
Primality Testing
"""


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

    methods = {'miller-rabin': miller_rabin_prime_test,
               'fermat': fermat_prime_test,
               'solovay-strassen': solovay_strassen_prime_test,
               }

    # TODO: Speed this up by using a prime sieve for small numbers
    # Handle some easy edge cases up front
    if x == 2 or x == 3:
        return True
    if x < 2 or x % 2 == 0:
        return False

    return methods[method](x)


def miller_rabin_decompose(n):
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


def miller_rabin_is_witness(potential_witness, n, power, remainder):
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


def miller_rabin_prime_test(x, attempts=25):
    """
        Implements the Miller Rabin primality test
    """
    # Find 2^s as the largest power of two that divides x-1
    power, remainder = miller_rabin_decompose(x - 1)
    for _ in range(attempts):
        # Generate a random potential witness
        potential_witness = random.randint(2, x - 2)
        if miller_rabin_is_witness(potential_witness, x, power, remainder):
            # If we find a witness, the given number is definitely not prime
            return False
    # If we make it through the witness testing, the number is probably prime
    return True


def fermat_prime_test(x, attempts=25):
    """
        Implements the Fermat primality (compositeness) test
    """
    for _ in range(attempts):
        a = random.randint(1, x - 1)
        if pow(a, x - 1, x) != 1:
            return False
    return True


def solovay_strassen_prime_test(n, attempts=25):
    """
        Implements the Solovay-Strassen primality test
    """
    for _ in range(attempts):
        a = random.randint(2, n - 1)
        x = jacobi(a, n)
        if pow(a, (n - 1) // 2, n) != x % n:
            return False
    return True


"""
Integer Factoring
"""


def factor(num, method):
    """
        Factor a number with the given method. Available methods are:

        'fermat'
        'pollard-rho'
        'pollard-p1'
        'gnu-factor'
        'trial-division'

        Example:
    """
    methods = {'fermat': fermat_factor,
               'pollard-rho': pollard_rho_factor,
               'pollard-p1': pollard_p1_factor,
               'gnu-factor': gnu_factor,
               'trial-division': trial_division_factors}
    return methods[method](num)


def fermat_factor(num):
    """
        Implements Fermat's Factoring Algorithm
    """
    if num < 2:
        return []
    elif num % 2 == 0:
        return [2] + fermat_factor(num // 2)
    elif gmpy2.is_prime(num):
        return [num]

    a = gmpy2.isqrt(num)
    b2 = gmpy2.square(a) - num

    while not gmpy2.is_square(b2):
        a += 1
        b2 = gmpy2.square(a) - num

    p = int(a + gmpy2.isqrt(b2))
    q = int(a - gmpy2.isqrt(b2))

    # Both p and q are factors of num, but neither are necessarily prime factors.
    # The case where p and q are prime is handled by the recursion base case.
    return fermat_factor(p) + fermat_factor(q)


def pollard_g(x, num):
    """The function g(a) = a^2 + 1 (mod n) of the Pollard Rho algorithm"""
    return int(gmpy2.square(x) + 1) % num


def pollard_f(x, num):
    """The function g(a) = a^2 - 1 (mod n) of the Pollard Rho algorithm"""
    return int(gmpy2.square(x) - 1) % num


def pollard_rho_factor(num, f=pollard_g):
    """
        Implements the Pollard Rho factorization algorithm. Passes in the function to use
        to make recursion easier.
    """

    if num < 2:
        return []
    elif num % 2 == 0:
        return [2] + pollard_rho_factor(num // 2)
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
    # if d == num and f == pollard_f:
    #     # either failure, or num is prime.
    #     return [d]
    # # Otherwise keep trying and hope the random `a` and `c` fix the issue

    # If we fail using the better function g, try the less better function f.
    if d == num and f == pollard_g:
        return pollard_rho_factor(num, pollard_f)
    # Finally, recurse to find *all* factors
    return pollard_rho_factor(d) + pollard_rho_factor(num // d)


def pollard_p1_factor(num, a=2):
    """
        Implements the Pollard P-1 factoring algorithm. Passes in the value of a to use
        to make recursion easier.
    """
    # Handle recursion base cases
    if num < 2:
        return []
    elif num % 2 == 0:
        return [2] + pollard_p1_factor(num // 2)
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
        return pollard_p1_factor(d) + pollard_p1_factor(num // d)
    # BUG: Occaisionally we get here and lose a factor or five.
    # FIX: Try again with a bigger a.
    return pollard_p1_factor(num, a + 1)


def gnu_factor(num):
    """
        Calls the GNU factor command. To be considered more authoritative.
    """
    if platform.system() != 'Linux':
        raise NotImplementedError('Cannot call GNU factor on non-Linux platform')
    output = subprocess.run(['factor', str(num)], stdout=subprocess.PIPE).stdout.decode('ascii')
    return list(map(int, output.strip().split()[1:]))


def trial_division_factors(num):
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
