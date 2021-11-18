# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 11:54:01 2020

@author: Administrator
"""


import geopandas
import pandas
import os

# set working space
os.chdir(r'H:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Sept\NRCan_python_Sept')
os.getcwd()

centroids = pandas.read_csv('Result/Control_points.csv', sep=',')
centroids_gdf = geopandas.GeoDataFrame(centroids, geometry=geopandas.points_from_xy(centroids.lon_4617, centroids.lat_4617))
footprint_gdf = geopandas.GeoDataFrame.from_file('Data/Projects_Footprints.shp')

studyarea = geopandas.GeoDataFrame.from_file('Data/StudyArea.shp')
hrdem = geopandas.GeoDataFrame.from_file('Data/hrdem.shp')

base = studyarea.plot(color='white', edgecolor='black')
hrdem.plot(ax=base, color='white', edgecolor='blue')
centroids_gdf.plot(ax=base, marker='*', color='green', markersize=5)