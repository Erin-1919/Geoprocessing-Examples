# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:35:09 2020

@author: Administrator
"""

# https://rpy2.github.io/doc/v2.9.x/html/introduction.html


## Start
# get versions
import rpy2
print(rpy2.__version__)
from rpy2.rinterface import R_VERSION_BUILD
print(R_VERSION_BUILD)


## rpy2 is providing 2 levels of interface with R: - low-level (rpy2.rinterface) - high-level (rpy2.robjects)
## The high-level interface is trying to make the use of R as natural as possible for a Python user 
import rpy2.robjects as robjects


## import R packages
from rpy2.robjects.packages import importr
# import R's "base" package
base = importr('base')
# import R's "utils" package
utils = importr('utils')


## Install R packages
# import rpy2's package module
import rpy2.robjects.packages as rpackages
# import R's utility package
utils = rpackages.importr('utils')
# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list
# R package names
packnames = ('ggplot2', 'hexbin')
# R vector of strings
from rpy2.robjects.vectors import StrVector
# Selectively install what needs to be install.
# We are fancy, just because we can.
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    utils.install_packages(StrVector(names_to_install))
    

## Evaluating R code
# The object r is also callable, and the string passed in a call is evaluated as R code.
import rpy2.robjects as robjects
# Under the hood, the variable pi is gotten by default from the R base package
pi = robjects.r['pi']
# pi is not a scalar but a vector of length 1
print (pi[0])
# calculate pi+2
pi_plus2 = robjects.r('pi')[0] + 2
print (pi_plus2)

# The string is a snippet of R code (complete with comments) that first creates an R function, 
# then binds it to the symbol f (in R), finally calls that function f. 
#The results of the call (what the R function f is returns) is returned to Python.
robjects.r('''
        # create a function `f`
        f <- function(r, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }
            2 * pi * r
        }
        # call the function `f` with argument value 3
        f(3)
        ''')

# Two ways to assign R function 'f' to Python function r_f
r_f = robjects.globalenv['f']
r_f = robjects.r['f']
print (r_f(3))


## Creating rpy2 vectors
# string vector
res = robjects.StrVector(['abc', 'def'])
print(res.r_repr())
# integer vector
res = robjects.IntVector([1, 2, 3])
print(res.r_repr())
# float vector
res = robjects.FloatVector([1.1, 2.2, 3.3])
print(res.r_repr())

# R matrixes and arrays are just vectors with a dim attribute
v = robjects.FloatVector([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
m = robjects.r['matrix'](v, nrow = 2)
print(m)


## Calling R functions
# By default, calling R functions return R objects.
# Calling R functions is similar to calling Python functions
rsum = robjects.r['sum']
rsum(robjects.IntVector([1,2,3]))[0]
# Keywords are also working
rsort = robjects.r['sort']
res = rsort(robjects.IntVector([1,2,3]), decreasing=True)
print(res.r_repr())


## Demo example
from rpy2.robjects.packages import importr
graphics = importr('graphics')
grdevices = importr('grDevices')
base = importr('base')
stats = importr('stats')

import array

x = array.array('i', range(10))
y = stats.rnorm(10)

grdevices.X11()

graphics.par(mfrow = array.array('i', [2,2]))
graphics.plot(x, y, ylab = "foo/bar", col = "red")

kwargs = {'ylab':"foo/bar", 'type':"b", 'col':"blue", 'log':"x"}
graphics.plot(x, y, **kwargs)


m = base.matrix(stats.rnorm(100), ncol=5)
pca = stats.princomp(m)
graphics.plot(pca, main="Eigen values")
stats.biplot(pca, main="biplot")


## Try DGGRID
from rpy2.robjects.packages import importr
dggridR = importr('dggridR')

import rpy2.robjects as robjects
# define orientation parameters
v_lat = 37.6895
v_lon = -51.6218
azimuth = 360-72.6482
# call R functions
py_dgconstruct = robjects.r['dgconstruct']
py_dgGEO_to_SEQNUM = robjects.r['dgGEO_to_SEQNUM']
py_dgSEQNUM_to_GEO = robjects.r['dgSEQNUM_to_GEO']
# define a function to convert geographic lat/lon to cell centroid position
def geo_to_centroid(resoluation, lon, lat):
    DGG = py_dgconstruct(projection = "ISEA", aperture = 3, topology = "HEXAGON", res = resoluation, 
                         precision = 7, azimuth_deg =  azimuth, pole_lat_deg = v_lat, pole_lon_deg = v_lon)
    Cell_address = py_dgGEO_to_SEQNUM(DGG,lon,lat)[0][0]
    lon_c_4326 = py_dgSEQNUM_to_GEO(DGG,Cell_address)[0][0]
    lat_c_4326 = py_dgSEQNUM_to_GEO(DGG,Cell_address)[1][0]
    return lon_c_4326,lat_c_4326

# test the new function
print (geo_to_centroid(20, 58, -41))
