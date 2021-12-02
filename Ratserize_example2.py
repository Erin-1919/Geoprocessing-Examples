# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:59:52 2021

@author: mingke.li
"""

import gdal
import ogr

fn_ras = 'path/to/raster'
fn_vec = 'path/to/vector'

out_net = 'path/to/outnet'

ras_ds = gdal.Open(fn_ras)
vec_ds = gdal.Open(fn_vec)
lyr = vec_ds.GetLayer()


geot = ras_ds.GetGeoTransform()

drv_tiff = gdal.GetDriverByName("GTiff")
chn_ras_ds = drv_tiff.Create(out_net, ras_ds.RasterXSize, ras_ds.RasterYSize, 1, gdal.GDT_Float32)
chn_ras_ds.SetGeoTransform(geot)

gdal.RasterizeLayer(chn_ras_ds, [1], lyr)
chn_ras_ds.GetRasterBand(1).SetNoDataValue(0.0)
chn_ras_ds = None

gdal.RasterizeLayer(chn_ras_ds, [1], lyr, options=['ATTRIBUTE=chn_id'])
chn_ras_ds.GetRasterBand(1).SetNoDataValue(0.0)
chn_ras_ds = None
