# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 12:43:07 2021

@author: mingke.li
"""

import numpy as np
import matplotlib.pyplot as plt
from time import time

def get_calories_burned(lower_temp, upper_temp, avg_tol, sd_tol, avg_calories_burned):
    temp = np.random.uniform(lower_temp,upper_temp)
    tol = np.random.normal(avg_tol, sd_tol)
    if temp > tol:
        cals = np.random.exponential(avg_calories_burned)
    else:
        cals = 0
    return cals

get_calories_burned(40,60,55,5,200)
daily_calories = []
num_days = 10000

start = time()
for _ in range(num_days):
    cals = get_calories_burned(40,60,55,5,200)
    daily_calories.append(cals)

end = time()
print (end-start)

plt.hist(daily_calories)
