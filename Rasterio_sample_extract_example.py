# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:50:55 2020

@author: Administrator
"""

# method 1

import rasterio
from rasterio.drivers import sample
from rasterio.plot import show

with rasterio.open(r'H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\example.tif') as src:
    x = (src.bounds.left + src.bounds.right) / 2.0 # -114.04822920000001
    y = (src.bounds.bottom + src.bounds.top) / 2.0 # 51.357395835
    vals = src.sample([(x, y)])
    for val in vals:
        print (list(val)) # [1105.15]
src.close()

# method 2
from osgeo import gdal
from numpy import array
# Read raster
source = gdal.Open(r'H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\example.tif')
nx, ny = source.RasterXSize, source.RasterYSize
gt = source.GetGeoTransform()
band_array = source.GetRasterBand(1).ReadAsArray()
# Close raster
source = None

from numpy import argmin, NAN
def nearest_neighbor(px, py, no_data=NAN):
    '''Nearest Neighbor point at (px, py) on band_array
    example: nearest_neighbor(2790501.920, 6338905.159)'''
    ix = int(round((px - (gt[0] + gt[1]/2.0))/gt[1]))
    iy = int(round((py - (gt[3] + gt[5]/2.0))/gt[5]))
    if (ix < 0) or (iy < 0) or (ix > nx - 1) or (iy > ny - 1):
        return no_data
    else:
        return band_array[iy, ix].astype(band_array.dtype)

print (nearest_neighbor(-114.04822920000001,51.357395835)) # 1105.15
