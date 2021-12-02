from scipy import ndimage
import numpy as np

####################################
a = np.array(([0,1,1,1,1],
                  [0,0,1,1,1],
                  [0,1,1,1,1],
                  [0,1,1,1,0],
                  [0,1,1,0,0]))

ndimage.distance_transform_edt(a)

####################################

# With a sampling of 2 units along x, 1 along y
ndimage.distance_transform_edt(a, sampling=[2,1])

####################################

# Asking for indices as well

edt, inds = ndimage.distance_transform_edt(a, return_indices=True)

####################################

# With arrays provided for inplace outputs

indices = np.zeros(((np.ndim(a),) + a.shape), dtype=np.int32)
ndimage.distance_transform_edt(a, return_indices=True, indices=indices)
                                   