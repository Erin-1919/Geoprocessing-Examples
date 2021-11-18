# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 18:22:57 2020

@author: Administrator
"""

import os
os.chdir(r'H:\UCalgary Courses\ENGO 697 Digital Earth\DowntownShapefiles')
os.environ['PROJ_LIB'] = r'C:\Users\Administrator\Documents\R\win-library\3.6\sf\proj'

import geopandas
point = geopandas.GeoDataFrame.from_file('TrafficCameras.shp') 
poly  = geopandas.GeoDataFrame.from_file('DowntownLandCover.shp')

from geopandas.tools import sjoin
pointInPolys = sjoin(point, poly, how='left')
grouped = pointInPolys.groupby('index_right')
print (grouped.groups)


# https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python/208574