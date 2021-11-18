# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:36:11 2020

@author: Administrator
"""

import os
#os.environ['GDAL_DATA'] = '/home/server/anaconda3/share/gdal'
os.environ['PROJ_LIB'] = r'C:\Users\Administrator\Documents\R\win-library\3.6\sf\proj'

#####Example 1 doesnt work!
from osgeo import ogr
from osgeo import osr

source = osr.SpatialReference()
source.ImportFromProj4("+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs")

target = osr.SpatialReference()
target.ImportFromProj4("+proj=longlat +datum=WGS84 +no_defs")

transform = osr.CoordinateTransformation(source, target)

point = ogr.CreateGeometryFromWkt("POINT (112.57 -50.42)")
point.Transform(transform)

print (point.ExportToWkt())

#####Example 2 it worked!
from pyproj import CRS
from pyproj import Transformer

crs_4326 = CRS.from_epsg(4326) #WGS84
crs_4326

crs_3160 = CRS.from_epsg(3160) #NAD83(CSRS) / UTM zone 16N
crs_3160

crs_4617 = CRS.from_epsg(4617) #NAD83(CSRS) geodetic
crs_4617

transformer = Transformer.from_crs(crs_4326, crs_3160)
transformer2 = Transformer.from_crs(crs_4326, crs_4617)

point = (46, -79) # lat, long

transformer.transform(*point)
transformer2.transform(*point)

#####Example 3 it worked!
import pyproj
from pyproj import CRS
from pyproj import Transformer
from pyproj.crs import CompoundCRS

cmpd_crs = CompoundCRS(name="WGS 84 + EGM96 height", components=["EPSG:4326", "EPSG:5773"])
trans = pyproj.Transformer.from_crs(cmpd_crs, "EPSG:4979") # epsg 4979 is Geographic 3D CRS 
trans.transform(45, -122, 10)


#####Example 4 it worked for lat/lon not height
import pyproj
from pyproj import CRS
from pyproj import Transformer
from pyproj.crs import CompoundCRS

cmpd_crs = CompoundCRS(name="WGS 84 + EGM96 height", components=["EPSG:4326", "EPSG:5773"])
trans = pyproj.Transformer.from_crs(cmpd_crs, "EPSG:5498") # EPSG:5498 NAD83 + NAVD88 height
trans.transform(45, -122, 10)


#####Try 1 doesn't work
import pyproj
from pyproj import CRS
from pyproj import Transformer
from pyproj.transformer import TransformerGroup

h1 = pyproj.crs.CompoundCRS(name="NAD83+HT2_0",components=["EPSG:4617","EPSG:5713"])
h2 = pyproj.crs.CompoundCRS(name="NAD83+cgvd2013",components=["EPSG:4617","EPSG:6647"])

tg = TransformerGroup(h1,h2)
tg

tg = TransformerGroup(h1,"EPSG:6649")
tg

h1 = CRS("urn:ogc:def:crs,crs:EPSG::4617,crs:EPSG::5713")
h2 = CRS("urn:ogc:def:crs,crs:EPSG::4617,crs:EPSG::6647")

transformer = pyproj.Transformer.from_crs(h1,h2)
transformer2 = pyproj.Transformer.from_crs(h1,"EPSG:6649")

transformer.transform(51.35770833, -114.0279167, 1083)
transformer2.transform(51.35770833, -114.0279167, 1083)

#####Try2 doesn't work
import pyproj
from pyproj import CRS
from pyproj import Transformer
from pyproj.transformer import TransformerGroup

v1 = pyproj.crs.VerticalCRS(name="CGVD28", datum="Canadian Geodetic Vertical Datum of 1928", geoid_model="HTv2.0")
c1 = pyproj.crs.CompoundCRS(name="NAD83+CGVD28",components=["EPSG:4617",v1])

v2 = pyproj.crs.VerticalCRS(name="CGVD2013", datum="Canadian Geodetic Vertical Datum of 2013", geoid_model="CGG2013a")
c2 = pyproj.crs.CompoundCRS(name="NAD83+CGVD2013",components=["EPSG:4617",v2])

TransformerGroup(c1,c2)

transformer = pyproj.Transformer.from_crs(c1,c2)
transformer.transform(45, -122, 10)









