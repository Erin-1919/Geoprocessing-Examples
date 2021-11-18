# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:32:53 2020

@author: Administrator
"""

import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show
import matplotlib.pyplot as plt

# Using rasterio with fiona, it is simple to open a shapefile, read geometries, 
# and mask out regions of a raster that are outside the polygons defined in the shapefile.

with fiona.open("box.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]


# This shapefile contains a single polygon, a box near the center of the raster, 
# so in this case, our list of features is one element long.

with rasterio.open("RGB_byte.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
    raster_data = src.read()
    
# Using plot and imshow from matplotlib, we can see the region defined by the shapefile 
# in red overlaid on the original raster.
plt.imshow(shapefile) # this line doesnt work
show(raster_data)

# Applying the features in the shapefile as a mask on the raster sets 
# all pixels outside of the features to be zero. 

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("RGB_byte_masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)


# visualize the result
with rasterio.open("RGB_byte_masked.tif") as dest:
    raster_data_out = dest.read()
    show(raster_data_out)