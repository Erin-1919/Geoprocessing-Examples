## in command line:  R CMD Rserve
## in python

# import pyRserve
import pyRserve
import numpy

# open pyRserve connection
conn = pyRserve.connect()

# A valid R command can be executed by making a call to the R name space via the connection's eval() method, 
# providing a string as argument which contains valid R syntax:
conn.eval('3 + 5')
# deliver back a floating point number
conn.eval('3 + 5', atomicArray=True)
# deliver back a real (numpy) array

# more examples
conn.eval("list(1, 'otto')")
conn.eval('c(1, 5, 7)')

# set a variable inside the R namespace do
conn.eval('aVar <- "abc"')
conn.eval('aVar')

# assign a python list with mixed data types to an R variable called aList
conn.r.aList = [1, 'abcde', numpy.array([1, 2, 3], dtype=int)]

# Numpy arrays can also contain dimension information which are translated into R matrices when assigned to the R namespace
arr = numpy.array(range(12))
arr.shape = (3, 4)
conn.r.aMatrix = arr
conn.r('dim(aMatrix)')

# create a function and execute it:
conn.voidEval('doubleit <- function(x) { x*2 }')
conn.eval('doubleit(2)')

# store a mini script definition in a Python string
my_r_script = '''
squareit <- function(x)
  { x**2 }
squareit(4)
'''

conn.eval(my_r_script)


# setting and accessing variables in a more Pythonic way
conn.r.aVar = "abc"
print('A value from R:', conn.r.aVar)

#load your rscript into a variable (you can even write functions)
test_r_script = '''
                library(foreign)
                dat<-read.spss("/path/spss_file.sav", 
                                 to.data.frame=TRUE)
                '''

#do the connection eval
variable = conn.eval(test_r_script)

print (variable)





## try with dggridR
dggridR_r_script = '''
                library(dggridR)
                DGG = dgconstruct(res=20)
                dgGEO_to_SEQNUM(DGG,45,45)
                '''

#do the connection eval
cellindex = conn.eval(dggridR_r_script)
print (cellindex)


dggridR_r_script2 = '''library(dggridR)'''
conn.eval(dggridR_r_script2)

conn.voidEval('''
geo_to_centroid <- function(resolution,lon,lat) {
  v_lat = 37.6895
  v_lon = -51.6218
  azimuth = 360-72.6482
  DGG = dgconstruct(projection = "ISEA", aperture = 3, topology = "HEXAGON", res = resolution, 
                       precision = 7, azimuth_deg =  azimuth, pole_lat_deg = v_lat, pole_lon_deg = v_lon)
  Cell_address = dgGEO_to_SEQNUM(DGG,lon,lat)$seqnum
  lon_c = dgSEQNUM_to_GEO(DGG,Cell_address)$lon_deg
  lat_c = dgSEQNUM_to_GEO(DGG,Cell_address)$lat_deg
  lon_lat = c(lon_c,lat_c)
  return (lon_lat)
}
'''
)

cellcentroid = conn.eval('geo_to_centroid(20,45,45)')
print (cellcentroid)


# closing the pyRserve connection
conn.close()