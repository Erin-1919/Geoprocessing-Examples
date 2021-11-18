# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:00:39 2020

@author: Administrator
"""

# Change working directory  
# import os   
# os.chdir(r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul")

import numpy as np

# Suppose we want to interpolate the 2-D function
def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

# Grid in [0, 1]x[0, 1], 100 rows and 200 columns
# Initialize grid_x and grid_y in the same way
grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

type(grid_x) # numpy.ndarray
type(grid_y) # numpy.ndarray

# Assume that we only know values at 1000 data points:
# Create an array of the given shape and populate it with random samples from 
# a uniform distribution over [0, 1).
points = np.random.rand(1000, 2) # an array of 1000 items of 2 dimensions
type(points) # numpy.ndarray

# Assign values to points, assume this is known
values = func(points[:,0], points[:,1])
type(values) # numpy.ndarray

# This can be done with griddata – below we try out all of the interpolation methods:
from scipy.interpolate import griddata
grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

# One can see that the exact result is reproduced by all of the methods to some degree, but for this smooth function the piecewise cubic interpolant gives the best results:
import matplotlib.pyplot as plt
plt.subplot(221)
plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
plt.plot(points[:,0], points[:,1], 'k.', ms=1)
plt.title('Original')
plt.subplot(222)
plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
plt.title('Cubic')
plt.gcf().set_size_inches(6, 6)
plt.show()

