# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:20:48 2020

@author: Administrator
"""

# Change working directory  
# import os   
# os.chdir(r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul")

import os
import gdal
import rasterio

os.environ['PROJ_LIB'] = r'C:\Users\Administrator\Documents\R\win-library\3.6\sf\proj'

dir_with_csvs = r"H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul"
os.chdir(dir_with_csvs)

# create .vrt file
def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith(suffix) ]
csvfiles = find_csv_filenames(dir_with_csvs)
for fn in csvfiles:
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tiff')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns" x="lon" y="lat" z="elev"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

# generate grids
output = gdal.Grid('CDEM_points_cgvd2013.tif','CDEM_points_cgvd2013.vrt',algorithm='nearest:radius1=0:radius2=0')

goption = gdal.GridOptions(format='GTiff', 
                           outputType=gdal.GDT_Float32,
                           width=640,height=336,
                           noData=-32767.0,
                           algorithm ="nearest:radius1=0:radius2=0",
                           layers="CDEM_points_cgvd2013")

output = gdal.Grid('CDEM_points_cgvd2013_2.tif','CDEM_points_cgvd2013.vrt', options = goption)

# check grids
raster_1 = rasterio.open("CDEM_raw.tif")
raster_1.meta
raster_1.res

raster_2 = rasterio.open("CDEM_points_cgvd2013.tif")
raster_2.meta
raster_2.res

# to have a negative y res is normal
# check https://gis.stackexchange.com/questions/243639/how-to-take-cell-size-from-raster-using-python-or-gdal-or-rasterio







