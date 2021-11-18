# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:54:50 2021

@author: mingke.li
"""

import os
os.chdir(r'G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Oct\NRCan_R_Oct\Test')

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import gc, numpy

polygons = gpd.GeoDataFrame.from_file('test1.shp')
polygons = polygons.rename(columns={"dummy":"cell_address"})
dem_df = pd.read_csv('test_dem.csv')

join_df = pd.merge(left = polygons, right = dem_df, how="left", on="cell_address")
join_df['model_elev'] = numpy.where(numpy.isnan(join_df['model_hrdem']), join_df['model_cdem'], join_df['model_hrdem'])
join_df = join_df.drop(columns=['model_cdem','model_hrdem'])

list(join_df.columns)
del polygons, dem_df
gc.collect()


fig, ax = plt.subplots()
join_df.plot(column='model_elev',ax=ax, cmap = 'gray', vmin = 0, vmax = 600, legend=True, figsize=(800, 800))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')
ax.axis("off")
plt.show()


# join_df.plot(column='model_elev',ax=ax, cmap = 'gray', vmin = 0, vmax = 600, scheme="User_Defined", 
#          legend=True, classification_kwds=dict(bins=[100,200,300,400,500,600]))