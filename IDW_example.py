import numpy as np

# inverse power to use
pow = 2

# some points:
known_pts = np.array([[0,0], [1,0], [3,0], [4,0],
                      [0,1], [2,1], [3,1], [4,1],
                      [1,3], [2,3], [3,3], [4,3]])

# and some data associated with them
known_values = known_pts[:,0] + known_pts[:,1]

# unknown points
unknown_pts = np.array([[2,0], [1,1], [0,2], [1,2], [2,2], [3,2], [4,2], [0,3]])

# calculate all distances from unknown points to known points:
# (the array will have as many rows as there are unknown points and as many columns
#  as there are known points)
dist = np.sqrt((known_pts[:,0][None,:]-unknown_pts[:,0][:,None])**2 + (known_pts[:,1][None,:]-unknown_pts[:,1][:,None])**2)

# calculate the inverse distances, use a small epsilon to avoid infinities:
idist = 1. / (dist + 1e-12)**pow

# calculate the weighted average for each column with idist as the weight function
unknown_values = np.sum(known_values[None,:] * idist, axis=1) / np.sum(idist, axis=1)

