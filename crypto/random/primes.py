import random
import gmpy2


# TODO: There's got to be a better implementation than this...
def random_prime(bits):
    """Generates a random prime number with `bits` bits"""
    # Generate a random number with n bits
    num = random.randint(10**(bits - 1) + 1, 10**bits)
    # Find the next prime after the number - will *probably* have n bits.
    return int(gmpy2.next_prime(num))
