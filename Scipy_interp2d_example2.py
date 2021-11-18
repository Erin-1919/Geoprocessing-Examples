# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 16:56:34 2020

@author: Administrator
"""

from osgeo import gdal
from numpy import array

# Read raster
source = gdal.Open(r'G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\example.tif')
nx, ny = source.RasterXSize, source.RasterYSize
gt = source.GetGeoTransform()
band_array = source.GetRasterBand(1).ReadAsArray()
# Close raster
source = None

# Compute mid-point grid spacings
ax = array([gt[0] + ix*gt[1] + gt[1]/2.0 for ix in range(nx)])
ay = array([gt[3] + iy*gt[5] + gt[5]/2.0 for iy in range(ny)])

# interpolation functions from scipy
from scipy import interpolate
bilinterp = interpolate.interp2d(ax, ay, band_array, kind='linear') # ind{‘linear’, ‘cubic’, ‘quintic’}, optional
cubicinterp = interpolate.interp2d(ax, ay, band_array, kind='cubic')
quinticinterp = interpolate.interp2d(ax, ay, band_array, kind='quintic')






# https://gis.stackexchange.com/questions/7611/bilinear-interpolation-of-point-data-on-a-raster-in-python
# customized fuction -- nearest_neighbor
from numpy import NAN
def nearest_neighbor(px, py, no_data=NAN):
    '''Nearest Neighbor point at (px, py) on band_array
    example: nearest_neighbor(2790501.920, 6338905.159)'''
    ix = int(round((px - (gt[0] + gt[1]/2.0))/gt[1]))
    iy = int(round((py - (gt[3] + gt[5]/2.0))/gt[5]))
    if (ix < 0) or (iy < 0) or (ix > nx - 1) or (iy > ny - 1):
        return no_data
    else:
        return band_array[iy, ix].astype(band_array.dtype)


# customized fuction -- bilinear
from numpy import floor, NAN
def bilinear(px, py, no_data=NAN):
    '''Bilinear interpolated point at (px, py) on band_array
    example: bilinear(2790501.920, 6338905.159)'''
    ny, nx = band_array.shape
    # Half raster cell widths
    hx = gt[1]/2.0
    hy = gt[5]/2.0
    # Calculate raster lower bound indices from point
    fx = (px - (gt[0] + hx))/gt[1]
    fy = (py - (gt[3] + hy))/gt[5]
    ix1 = int(floor(fx))
    iy1 = int(floor(fy))
    # Special case where point is on upper bounds
    if fx == float(nx - 1):
        ix1 -= 1
    if fy == float(ny - 1):
        iy1 -= 1
    # Upper bound indices on raster
    ix2 = ix1 + 1
    iy2 = iy1 + 1
    # Test array bounds to ensure point is within raster midpoints
    if (ix1 < 0) or (iy1 < 0) or (ix2 > nx - 1) or (iy2 > ny - 1):
        return no_data
    # Calculate differences from point to bounding raster midpoints
    dx1 = px - (gt[0] + ix1*gt[1] + hx)
    dy1 = py - (gt[3] + iy1*gt[5] + hy)
    dx2 = (gt[0] + ix2*gt[1] + hx) - px
    dy2 = (gt[3] + iy2*gt[5] + hy) - py
    # Use the differences to weigh the four raster values
    div = gt[1]*gt[5]
    return (band_array[iy1,ix1]*dx2*dy2/div +
            band_array[iy1,ix2]*dx1*dy2/div +
            band_array[iy2,ix1]*dx2*dy1/div +
            band_array[iy2,ix2]*dx1*dy1/div).astype(band_array.dtype)



# compare the results
# check boundaries
import rasterio
file = rasterio.open(r'G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul\example.tif')
file.bounds

x = -114.09
y = 51.33
vals = file.sample([(x, y)])
for val in vals:
    print (list(val)) # [1154.153]
        
    
print(bilinterp(-114.09,51.33))
print(cubicinterp(-114.09,51.33))
print(quinticinterp(-114.09,51.33))

print(nearest_neighbor(-114.09,51.33))
print(bilinear(-114.09,51.33))

