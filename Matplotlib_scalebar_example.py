# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:36:32 2021

@author: mingke.li
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib_scalebar.scalebar import ScaleBar

# Load image
with cbook.get_sample_data("s1045.ima.gz") as dfile:
    im = np.frombuffer(dfile.read(), np.uint16).reshape((256, 256))

# Create subplot
fig, ax = plt.subplots()
ax.axis("off")

# Plot image
ax.imshow(im, cmap="gray")

# Create scale bar
scalebar = ScaleBar(0.08, "cm", length_fraction=0.25)
ax.add_artist(scalebar)

# Show
plt.show()