""" 
Prime number iterator.

Implements basic trial division of a number up to its square root as the primality test.
Choosing a factor of 2 when looking for a larger prime number is based on Chebyshev's theorem that there is a prime number in the interval (n,2n] for int n > 0
"""
from __future__ import annotations
from collections.abc import Iterator
import math

__author__ = 'Code by Wong Jia Cheng'
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    """ 
        Computes and returns the largest prime number that is strictly less than the current value of the upper bound

        Attributes:
        * upper_bound (int) : prime number obtained must be less than this value
        * factor(int) : used to update upper bound to a larger value in each iteration

    """
    def __init__(self, upper_bound: int, factor: int) -> None:
        """ 
            Initialises attributes

            :param arg1: upper_bound - the upper bound of the prime

            :param arg2: factor

            :pre: upper_bound >= 3, so that the first prime number obtained is 2

            :return: None
            
            :complexity: Best = Worst = O(1)
        """
        # check that upper_bound is valid
        if upper_bound < 3:
            raise ValueError("Upper bound must be at least 3")
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self)-> Iterator[int]:
        """ 
            Standard __iter__() method for initialisers. Returns itself. 

            :param: None

            :pre: None

            :return: self
            
            :complexity: Best/Worst = O(1)
        """
        return self

    def __next__(self) -> int:
        """ 
            Returns the next prime number. It is the largest prime number less than upper bound.

            :param: None

            :pre: None

            :return: int - the next number of the iteratable object
            
            :complexity: O(N), where N is self.upper_bound
        """
        current = self.upper_bound 

        # start with upper_bound - 1 (the first value less than upper bound), and keep decrementing until a prime is found. 
        # Assuming the factor is 2, the prime will be between previous upper bound(N) and new upper bound(2N) so iterates a maximum of n times, hence O(N)
        # Chebyshev's theorem states that there is a prime number in the interval (n,2n] for int n > 0
        while True:
            current -= 1
            if self.is_prime(current): # when current is prime, stop
                break 

        self.upper_bound = current * self.factor # update upper bound for next call
        return current
    
    
    def is_prime(self, n: int) -> bool:
        """ 
            Primality test

            :param: n - the number I wish to investigate whether it is a prime or not

            :pre: None

            :return: boolean - True if it is prime
            
            :complexity: Best O(1) when n <= 2 or n is even or 
                         Worst O(sqrt(n)), when we need to test the divisibility (sqrt(n)+1 - 3) times
        """
        if n == 2:
            return True
        if (n < 2) or (n % 2 == 0): # if n is less than 2 or even it is not prime
            return False

        # For each odd integer(which is why we increment by two) in the range of 3 until the square root of n, check if it divides n
        # n is prime if and only if all of these integers do not divide n. 
        return not any(n % i == 0 for i in range(3, int(math.sqrt(n)) + 1, 2))
    
if __name__ == "__main__":
    it = LargestPrimeIterator(6,2)
    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))