import math
import gmpy2
from .primality import primes


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
    elif num % 2 == 0:
        return [2] + _fermat_factor(num // 2)
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
