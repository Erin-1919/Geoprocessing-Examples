# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:28:17 2021

@author: mingke.li
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

colours = ['#ffbe0b', '#fb5607', '#ff006e', '#8338ec', '#3a86ff']
bins = [0 , 0.3 , 0.7 , 1.75 , 1.9]

assert len(bins)== len(colours)
cmap = mpl.colors.ListedColormap(colours)
norm = mpl.colors.BoundaryNorm(boundaries=bins, ncolors=len(cmap.colors)-1 )

fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)
cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                boundaries= [-.1] + bins + [2.1],
                                extend='both',
                                ticks=bins,
                                spacing='proportional',
                                orientation='horizontal')
cb2.set_label('Custom colour bar')
plt.show()

x = np.linspace(0,2.5,100)
y = [np.random.random()*2 for i in range(100)]
size = 2 + (1.2-np.array(y))*2
plt.scatter(x,y,c=x,cmap=cmap,norm = norm)
plt.show()

