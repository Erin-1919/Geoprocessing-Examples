# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:21:18 2021

@author: Erin
"""

#####################
import os
os.chdir(r'G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Jul\NRCan_python_Jul')

import datashader as ds, pandas as pd, colorcet
from datashader.utils import export_image
from functools import partial

df = pd.read_csv('CDEM_points_cgvd2013.csv')
df = df[["lat","lon","height"]]

cvs = ds.Canvas(plot_width=300, plot_height=300)
agg = cvs.points(df, 'lon', 'lat', ds.mean('height'))
ds.tf.set_background(ds.tf.shade(agg, cmap=colorcet.CET_L10,how = "linear"), "white")

export = partial(export_image, background = "black", export_path="export")
export(ds.tf.shade(agg, cmap = colorcet.fire),"filename")

#####################
import datashader as ds, matplotlib.pyplot as plt
from datashader.mpl_ext import dsshow

fig, ax = plt.subplots()
artist = dsshow(df, ds.Point('lon', 'lat'), aggregator = ds.mean('height'), norm='eq_hist', cmap = colorcet.CET_L10, 
                vmin = 1000, vmax = 2000, plot_width=300, plot_height=300, ax = ax)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.axis("off")

plt.savefig('test2.png', bbox_inches='tight', pad_inches=0.0)



#import holoviews.operation.datashader as hd
#import holoviews as hv

#####################
import os
os.chdir(r'C:\Users\mingke.li\datashader-examples')

import datashader as ds, pandas as pd, colorcet as cc
from datashader.colors import Elevation
from datashader.utils import export_image
from functools import partial

df = pd.read_csv('data/nyc_taxi.csv', usecols=['dropoff_x', 'dropoff_y'])
df.head()
len(df) #10679307

# output an image with black backgroung, color shows the aggreated point count in each pixel
agg = ds.Canvas().points(df, 'dropoff_x', 'dropoff_y') # default agg function is count()
ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black") # https://colorcet.holoviz.org/user_guide/index.html
ds.tf.set_background(ds.tf.shade(agg, cmap=cc.CET_L10), "white")
ds.tf.set_background(ds.tf.shade(agg, cmap=Elevation), "white") # https://github.com/holoviz/datashader/blob/master/datashader/colors.py

agg = ds.Canvas().area(df, 'dropoff_x', 'dropoff_y') # obviously slow
ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")

# export image
export = partial(export_image, background = "white", export_path=".")
export(ds.tf.shade(agg, cmap=cc.CET_L10),"test.jpeg")


#####################
import os
os.chdir(r'C:\Users\mingke.li\datashader-examples')

import datashader as ds, pandas as pd, colorcet as cc, numpy as np
import xarray
from datashader.utils import export_image
from functools import partial

df = pd.read_csv('data/nyc_taxi.csv', usecols=['dropoff_x', 'dropoff_y'])
df1,df2,df3 = np.array_split(df, 3)

agg1 = ds.Canvas().points(df1, 'dropoff_x', 'dropoff_y') 
fig1 = ds.tf.shade(agg1, cmap=cc.CET_L10)

agg2 = ds.Canvas().points(df2, 'dropoff_x', 'dropoff_y') 
fig2 = ds.tf.shade(agg2, cmap=cc.CET_L11)

agg3 = ds.Canvas().points(df3, 'dropoff_x', 'dropoff_y') 
fig3 = ds.tf.shade(agg3, cmap=cc.CET_L10)

# dim_1 = pd.Index([1, 2, 3])
# agg = xarray.concat([agg1,agg2,agg3],dim=dim_1)
# ds.tf.set_background(ds.tf.shade(agg, cmap=cc.CET_L10), "white")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import gridspec

imgplot = plt.imshow(fig1).set_cmap('terrain') # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html

nrow = 3
ncol = 3

fig = plt.figure(figsize=(ncol+1, nrow+1)) 

gs = gridspec.GridSpec(nrow, ncol,
         wspace=0, hspace=0, 
         top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
         left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 

for i in range(nrow):
    for j in range(ncol):
        im = np.random.rand(28,28)
        ax= plt.subplot(gs[i,j])
        ax.imshow(fig1).set_cmap('terrain')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")

# handles, labels = ax.get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower left')

plt.show()


# making a zoomable interactive overlay on a geographic map
import holoviews as hv
from holoviews.element.tiles import EsriImagery,CartoLight,CartoEco
#https://holoviews.org/reference/elements/bokeh/Tiles.html
from holoviews.operation.datashader import datashade
hv.extension('bokeh')

map_tiles  = CartoLight().opts(alpha=0.5, width=900, height=480, bgcolor='black')
points     = hv.Points(df, ['dropoff_x', 'dropoff_y'])
taxi_trips = datashade(points, x_sampling=1, y_sampling=1, cmap=cc.fire, width=900, height=480)

map_tiles * taxi_trips
