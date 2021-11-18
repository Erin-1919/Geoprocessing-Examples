# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 13:20:18 2020

@author: Administrator
"""


## This recipe installs a GDAL error handler function that captures the GDAL error, class and message. 
## Only works with GDAL version >= 1.10
import sys,os
try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

# Enable GDAL/OGR exceptions
gdal.UseExceptions()
    

os.environ['GDAL_DATA'] = r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul"

# import libraries
from osgeo import ogr, osr
import os
import shapefile, csv

## Import data from csv file
# create a pointZ shapefile -- 3D points
point_shp = shapefile.Writer(r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\test1.shp", shapeType=11)
# for every record there must be a corresponding geometry.
point_shp.autoBalance = 1
# create the field names and data type for each.
point_shp.field("StationID", "C")
# point_shp.field("Elevation", "N")
# count the features
counter = 1

# access the CSV file
with open(r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\test1.csv", "rt", encoding="utf8") as csvfile:
 reader = csv.reader(csvfile, delimiter=',')
 # skip the header
 next(reader, None)

 # loop through each of the rows and assign the attributes to variables
 for row in reader:
  station_id = row[0]
  longitude = row[1]
  latitude = row[2]
  elevation = row[3]

  # create the point geometry
  point_shp.pointz(float(longitude),float(latitude),int(elevation))
  # add attribute data
  point_shp.record(station_id)

  print ("Feature " + str(counter) + " added to Shapefile.")
  counter += 1

point_shp.close()

# test
# r = shapefile.Reader('test1.shp')
# r.shape(0).z
# r.shape(1).z
# r.shape(2).z
# r.shape(3).z

# r.close()