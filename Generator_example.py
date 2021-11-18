# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 12:50:58 2021

@author: mingke.li
"""

def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
        
gen = infinite_sequence()
next(gen)


def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

f = fib(6)
next(f)
