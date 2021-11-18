# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 08:17:22 2020

@author: Administrator
"""

# Change working directory  
# import os   
# os.chdir(r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul")

import rasterio
from rasterio.enums import Resampling

# Here is an example of upsampling by a factor of 2 using the bilinear resampling method.
# Downsampling to 1/2 of the resolution can be done with upscale_factor = 1/2.
upscale_factor = 2

with rasterio.open("example.tif") as dataset:
    print ("width:" + str(dataset.width))
    print ("height:" + str(dataset.height))
    print ("bounds:")
    print (dataset.bounds)
    
    # resample data to target shape
    data = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height * upscale_factor),
            int(dataset.width * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])
    )
    
# Of note, the default nearest method may not be suitable for continuous data. 
# In those cases, bilinear and cubic are better suited. 
# Some specialized statistical resampling method exist, e.g. average, 
# which may be useful when certain numerical properties of the data are to be retained.

# Write to a new dataset and save it
# Copy the metadata
out_meta = dataset.meta.copy()

# Update the metadata
out_meta.update({"driver": "GTiff",
                 "height": data.shape[-2],
                 "width": data.shape[-1],
                 "count":1,
                 "dtype": data.dtype,
                 "transform": transform,
                 "crs": "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs"
                 }
                )

#new_dataset = rasterio.open('example_output.tif','w', driver='GTiff', height=data.shape[-2], width=data.shape[-1], count=1, dtype=data.dtype, crs='+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs', transform=transform)

new_dataset = rasterio.open('example_output.tif','w',**out_meta)
new_dataset.write(data)
new_dataset.close()
        
# check
with rasterio.open("example_output.tif") as newdt:
    print ("width:" + str(newdt.width))
    print ("height:" + str(newdt.height))
    print ("bounds:")
    print (newdt.bounds)

newdt.close()

# Visualization
from rasterio.plot import show
show(data, cmap='terrain')

# from osgeo import gdal
# # Open raster and get band
# in_ds = gdal.Open('example_output.tif')
# in_band = in_ds.GetRasterBand(1)
# in_band.YSize
# in_band.XSize