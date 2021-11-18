# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:54:45 2020

@author: Administrator
"""

import os
os.chdir(r'H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul')

## With PyQGIS

ras  = QgsRasterLayer("example.tif")
pixelSizeX= ras.rasterUnitsPerPixelX()
pixelSizeY = ras.rasterUnitsPerPixelY()
print (pixelSizeX)
print (pixelSizeY)

## With GDAL

from osgeo import gdal
raster = gdal.Open('example.tif')
gt =raster.GetGeoTransform()
print (gt)
pixelSizeX = gt[1]
pixelSizeY =-gt[5]
print (pixelSizeX)
print (pixelSizeY)

## With rasterio

import rasterio
raster =  rasterio.open('example.tif')
gt = raster.transform
print (gt)
pixelSizeX = gt[0]
pixelSizeY =-gt[4]
print (pixelSizeX)
print (pixelSizeY)

# to have a negative y res is normal
# check https://gis.stackexchange.com/questions/243639/how-to-take-cell-size-from-raster-using-python-or-gdal-or-rasterio
