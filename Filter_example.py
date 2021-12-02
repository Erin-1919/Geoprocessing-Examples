# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:34:44 2021

@author: mingke.li
"""

def is_odd(n):
    return n % 2 == 1

filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])
type(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))

def not_empty(s):
    return s and s.strip()

list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))




def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
        
def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter() # initial sequence
    while True:
        n = next(it) # the first item of the seq
        yield n
        it = filter(_not_divisible(n), it) # conduct new seq

for n in primes():
    if n < 1000:
        print(n)
    else:
        break
    


a = _odd_iter()
next(a)
