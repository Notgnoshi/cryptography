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
    """
        Computes the modular inverse of an integer matrix, by computing the regular matrix inverse,
        then bultiplying by the determinant and the determinant's modular inverse before reducing
        modulo the given modulus.

        Example:
        >>> m = numpy.matrix([[1, 2], [3, 4]])
        >>> m_inv = modular_matrix_inverse(m, 5)
        >>> m_inv
        matrix([[ 3.,  1.],
                [ 4.,  2.]])
        >>> numpy.mod(numpy.matmul(m, m_inv), 5)
        matrix([[ 1.,  0.],
                [ 0.,  1.]])
    """

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
        Yields the numbers from 1 to `num` that are coprime with `num` by checking the gcd of
        every number between 0 and `num`.

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
        A generator that yields the first `limit` primes. If `limit` is not specified, the generator
        will yield infinitely many primes.

        Implemented by using gmpy2.next_prime() to generate prime after prime.

        Example:
        >>> p = primes(10)
        >>> list(p)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    return itertools.islice(_primes(), limit)


def legendre(a, p):
    """
        The Legendre Symbol of `a` mod `p`. Implementing by raising `a` to the `(p - 1) / 2` power
        mod `p`.

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

        Implemented by factoring `a` and multiplying powers of each factor's Legendre symbol to get
        the Jacobi Symbol of `a`.

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

        Implemented via the Tonelli-Shanks algorithm.

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
        Yields the primitive roots of the composite number `n`. Note that our textbook only defines
        primitive roots modulo some prime `p`. This implementation accepts the Wikipedia definition
        that defines primitive roots for composite numbers as well.

        Note that this definition is consistent with an implementation that only accepts prime
        modulus's.

        Implemented by finding the set of coprimes of `n` and checking if the set of powers is
        equal to the set of coprimes for each number a in 1..n

        Example:
        >>> list(primitive_roots(11))
        [2, 6, 7, 8]
    """
    # Wikipedia defines coprime for a composite number using the coprimes of that number,
    # while our textbook uses all numbers up to a prime `p`. For generality prefer composite `n`.
    cop = set(coprimes(n))
    for a in cop:
        if set(pow(a, x, n) for x in range(1, n)) == cop:
            yield a


def is_primitive_root(a, p):
    """
        Determine if `a` is a primitive root mod a prime number `p` by brute force checking all of
        the modular powers a^x (mod p) for x < p.

        Example:
        >>> is_primitive_root(3, 13)
        False
        >>> is_primitive_root(2, 13)
        True
    """
    return set(pow(a, x, p) for x in range(1, p)) == set(range(1, p))


def wheel_sieve():
    """
        A recursive generator implementation of the wheel factorization sieve. This implementation
        merges the wheel factorization algorithm with the sliding infinite sieve algorithm
        presented at https://stackoverflow.com/a/19391111.

        Example:
        >>> sieve = wheel_sieve()
        >>> next(sieve)
        11
        >>> next(sieve)
        13
    """
    wheel_11 = [2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2,
                4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10]
    cycle_sieve = itertools.accumulate(itertools.chain([11], itertools.cycle(wheel_11)))
    yield next(cycle_sieve)
    prime_sieve = wheel_sieve()
    prime = next(prime_sieve)
    p2 = prime ** 2
    d = dict(zip(itertools.accumulate(itertools.chain([0], wheel_11)), itertools.count(0)))
    multiples = {}
    for candidate in cycle_sieve:
        if candidate in multiples:
            wheel = multiples.pop(candidate)
        elif candidate < p2:
            yield candidate
            continue
        else:
            i = d[(prime - 11) % 210]
            wheel = itertools.accumulate(itertools.chain(
                [p2], itertools.cycle([prime * j for j in wheel_11[i:] + wheel_11[:i]])))
            next(wheel)
            prime = next(prime_sieve)
            p2 = prime ** 2
        for m in wheel:
            if m not in multiples:
                break
            multiples[m] = wheel


def wheel_factorization():
    """
        Implements Wheel Factorization to yield primes

        Example:
        >>> primes = wheel_factorization()
        >>> tuple(itertools.islice(primes, 10))
        (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    """
    return itertools.chain((2, 3, 5, 7), wheel_sieve())


def sundaram_sieve(n):
    """
        Implements the Sieve of Sundaram to yield primes smaller than the given `n`

        Example:
        >>> sundaram_sieve(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
    """
    limit = (n - 2) // 2
    sieve = numpy.full(n, True, dtype=bool)
    for i in range(1, limit // 2):
        for j in range(i, limit // 2):
            index = i + j + 2 * i * j
            if index <= n:
                sieve[index] = False
            else:
                break

    # Primes have the form 2i + 1 where i is the index of the nonmarked numbers
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]


def eratosthenes_sieve(limit):
    """
        Implements the Sieve of Eratosthenes to yield primes less than `limit`

        Example:
        >>> eratosthenes_sieve(10)
        [2, 3, 5, 7]
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
        or 'solovay-strassen'.

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
    if x < 2 or x % 2 == 0 or x % 3 == 0:
        return False

    return methods[method](x)


def miller_rabin_decompose(n):
    """
        Decomposes the given even integer into some power of two and some remainder

        Example:
        >>> miller_rabin_decompose(18)  # (2 ^ 1) * 9 = 18
        (1, 9)
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
        Implements the Miller Rabin primality test, using 25 attempts by default.

        Example:
        >>> miller_rabin_prime_test(1729)
        False
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
        Implements the Fermat primality (compositeness) test. Note that if this function returns
        True, the number is *probably* prime, but if the function returns False, the number is
        definitely composite.

        Example:
        >>> fermat_prime_test(1792)
        False
    """
    for _ in range(attempts):
        a = random.randint(1, x - 1)
        if pow(a, x - 1, x) != 1:
            return False
    return True


def solovay_strassen_prime_test(n, attempts=25):
    """
        Implements the Solovay-Strassen primality test. Works bu computing the Jacobi symbol of a
        random number, and compares a modular power of the given number to the Jacobi symbol (mod n)

        Example:
        >>> solovay_strassen_prime_test(1729)
        False
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
        'gnu-factor' -- must be using Linux with `factor` installed
        'trial-division'

        Almost all methods are recursive and use a primality check as a base case. This may be
        inefficient, but several of the methods factor a number n into two numbers p and q, of
        which, while both are factors, only one will be prime. Recursion was also necessary to
        completely factor numbers into their prime factors.

        Note that these are probabilistic factorings, and will not always have the same ordering.

        Example:

        >>> factor(10, 'trial-division')
        [2, 5]
        >>> factor(1729, 'pollard-rho')
        [7, 19, 13]
        >>> factor(1729, 'pollard-p1')
        [7, 13, 19]
        >>> factor(1729, 'fermat')
        [13, 7, 19]
        >>> factor(123465762, 'gnu-factor')
        [2, 3, 3, 3, 7, 19, 17191]
    """
    methods = {'fermat': fermat_factor,
               'pollard-rho': pollard_rho_factor,
               'pollard-p1': pollard_p1_factor,
               'gnu-factor': gnu_factor,
               'trial-division': trial_division_factors}
    return methods[method](num)


def fermat_factor(num):
    """
        Implements Fermat's Factoring Algorithm.

        Implemented recursively because just one call will produce two factors, only one of which
        is prime. Uses a primality test as one of the base cases.

        Example:
        >>> fermat_factor(1723)
        [1723]
        >>> fermat_factor(1729)
        [13, 7, 19]
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

        Implemented recursively, because the pollard rho algorithm only splits a number into two
        factors, only one of which is necessarily prime.

        Example:
        >>> pollard_rho_factor(1729)
        [7, 19, 13]
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

    # If we fail using the better function g, try the less better function f.
    if d == num and f == pollard_g:
        return pollard_rho_factor(num, pollard_f)
    # Finally, recurse to find *all* factors
    return pollard_rho_factor(d) + pollard_rho_factor(num // d)


def pollard_p1_factor(num, a=2):
    """
        Implements the Pollard P-1 factoring algorithm. Passes in the value of a to use
        to make recursion easier.

        Implemented recursively. If the previous attempt fails, try again with an incremented `a`.

        Example:
        >>> pollard_p1_factor(1729)
        [7, 13, 19]
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

    if d is not None:
        return pollard_p1_factor(d) + pollard_p1_factor(num // d)
    return pollard_p1_factor(num, a + 1)


def gnu_factor(num):
    """
        Calls the GNU factor command. To be considered more authoritative for small enough inputs.

        While other implementations might work in theory for large inputs, the GNU factor
        implementation will definitely work quite quickly for "small" inputs.

        Example:
        >>> gnu_factor(12346512786934827632345612323422)
        [2, 3, 3, 3, 3, 7, 73, 28515367, 5230334088831978263]
    """
    if platform.system() != 'Linux':
        raise OSError('Cannot call GNU factor on non-Linux platform')
    output = subprocess.run(['factor', str(num)], stdout=subprocess.PIPE).stdout.decode('ascii')
    return list(map(int, output.strip().split()[1:]))


def trial_division_factors(num):
    """
        Implements naive trial division to factor a given number. The simplest of the factorization
        implementations, but also the slowest.

        Example:
        >>> trial_division_factors(23142)
        [2, 3, 7, 19, 29]
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
