import gmpy2
import math
import random


class NumberTheory(object):
    """A utility class for common number theory operations"""

    @classmethod
    def coprimes(cls, n):
        """Yields the numbers from 0 to n that are coprime with n."""
        return iter(filter(lambda x: math.gcd(x, n) == 1, range(n)))

    @classmethod
    def prime_pi(cls, n):
        """Returns the number of primes less than n"""
        return n / math.log(n)

    @classmethod
    def random_prime(cls, n):
        """Generates a random large prime number with n digits"""
        # Generate a random number with n digits
        num = random.randint(10**(n - 1) + 1, 10**n)
        # Find the next prime after the number - will *probably* have n digits.
        return gmpy2.next_prime(num)

    @classmethod
    def is_prime(cls, x):
        """Returns True if x is probably prime, False otherwise. Runs 25 Miller-Rabin tests."""
        return gmpy2.is_prime(x, 25)
