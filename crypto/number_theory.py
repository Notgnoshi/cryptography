import math


class NumberTheory(object):
    """A utility class for common number theory operations"""

    @classmethod
    def coprimes(cls, n):
        """Yields the numbers from 0 to n that are coprime with n."""
        return iter(filter(lambda x: math.gcd(x, n) == 1, range(n)))

    @classmethod
    def prime_pi(n):
        """Returns the number of primes less than n"""
        return n / math.log(n)
