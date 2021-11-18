# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:09:34 2020

@author: Administrator
"""

# https://rtree.readthedocs.io/en/latest/tutorial.html
# https://toblerity.org/rtree/examples.html

import rtree
from rtree import index

# After importing the index module, construct an index with the default construction
idx = index.Index()

# Create a bounding box
left, bottom, right, top = (0.0, 0.0, 1.0, 1.0)

# Insert records into the index
idx.insert(0, (left, bottom, right, top))

## Query the index

# Intersection
# Given a query window, return ids that are contained within the window
list(idx.intersection((1.0, 1.0, 2.0, 2.0)))
# Given a query window that is beyond the bounds of data we have in the index:
list(idx.intersection((1.0000001, 1.0000001, 2.0, 2.0)))

# Nearest Neighbors
# The following finds the 1 nearest item to the given bounds. If multiple items are of equal distance to the bounds, both are returned:
idx.insert(1, (left, bottom, right, top))
list(idx.nearest((1.0000001, 1.0000001, 2.0, 2.0), 1))

## Using Rtree as a cheapo spatial database
# Rtree also supports inserting any object you can pickle into the index (called a clustered index in libspatialindex parlance).
# The following inserts the picklable object 42 into the index with the given id
idx.insert(4321, (left, bottom, right, top), obj=42)

# You can then return a list of objects by giving the objects=True flag to intersection
[n.object for n in idx.intersection((left, bottom, right, top), objects=True)]


## Serializing your index to a file
file_idx = index.Rtree('rtree')
file_idx.insert(1, (left, bottom, right, top))
file_idx.insert(2, (left - 1.0, bottom - 1.0, right + 1.0, top + 1.0))
[n for n in file_idx.intersection((left, bottom, right, top))]

## Modifying file names
p = rtree.index.Property()
p.dat_extension = 'data'
p.idx_extension = 'index'
file_idx = index.Index('rtree', properties = p)

