# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:00:20 2020

@author: Administrator
"""

import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

dem_fps = ["dtm_1m_utm11_e_20_169.tif","example_output.tif"]

src_files_to_mosaic = []
for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)
    
# Visualization
show(src_files_to_mosaic[0], cmap='terrain')
show(src_files_to_mosaic[1], cmap='terrain')

# Merge function returns a single mosaic array and the transformation info
# rasterio.merge.merge(datasets, bounds=None, res=None, nodata=None, dtype=None, 
                    #precision=10, indexes=None, output_count=None, 
                    #resampling=<Resampling.nearest: 0>, method='first')
mosaic, out_trans = merge(src_files_to_mosaic, method='first')

# Plot the result
show(mosaic, cmap='terrain')

# Copy the metadata
out_meta = src.meta.copy()

# Update the metadata
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "crs": "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs"
                 }
                )

# Write the mosaic raster to disk
with rasterio.open("mosaic_output", "w", **out_meta) as dest:
    dest.write(mosaic)