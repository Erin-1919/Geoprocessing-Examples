import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# some 3-dim points
mean = np.array([0.0,0.0,0.0])
cov = np.array([[1.0,-0.5,0.8], [-0.5,1.1,0.0], [0.8,0.0,1.0]])
data = np.random.multivariate_normal(mean, cov, 50)

# regular grid covering the domain of the data
X,Y = np.meshgrid(np.arange(-3.0, 3.0, 0.5), np.arange(-3.0, 3.0, 0.5))
XX = X.flatten()
YY = Y.flatten()

order = 1    # 1: linear, 2: quadratic
if order == 1:
    # best-fit linear plane
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients
    
    # evaluate it on grid
    Z = C[0]*X + C[1]*Y + C[2]
    
    # or expressed using matrix/vector product
    #Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

elif order == 2:
    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])
    
    # evaluate it on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)

# plot points and fitted surface
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
plt.xlabel('X')
plt.ylabel('Y')
ax.set_zlabel('Z')
# ax.axis('equal')
# ax.axis('tight')
plt.show()






import numpy as np
from itertools import combinations
import scipy.linalg
x = [1.2, 1.3, 1.6, 2.5, 2.3, 2.8]
y = [167.0, 180.3, 177.8, 160.4, 179.6, 154.3]
z = [-0.3, -0.8, -0.75, -1.21, -1.65, -0.68]
f = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]).transpose()

G = np.c_[x, y, z]

A = np.concatenate((G, np.ones((G.shape[0],1))), axis=1)
C, _, _, _ = scipy.linalg.lstsq(A, f)
# C will have now the coefficients for:
# f(x, y, z) = ax + by + cz + d

# quadratic eq.
dim = G.shape[1]
A = np.concatenate((G**2, np.array([np.prod(G[:, k], axis=1) for k in combinations(range(dim), dim-1)]).transpose(), G, np.ones((G.shape[0], 1))), axis=1)
C, _, _, _ = scipy.linalg.lstsq(A, f)
# C will have now the coefficients for:
# f(x, y, z) = ax**2 + by**2 + cz**2 + dxy+ exz + fyz + gx + hy + iz + j

# This can be used then:
def quadratic(a):
    dim = a.shape[0]
    A = np.concatenate((a**2, np.array([np.prod(a[k,]) for k in combinations(range(dim), dim-1)]), a, [1]))
    return np.sum(np.dot(A, C))

for i in range(G.shape[0]):
    print(quadratic(G[i,:]), f[i])
    
    
    
import math
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

x_ls = [0,0,1,1,0,-1,-1]
y_ls = [0,math.sqrt(3)/3*2,math.sqrt(3)/3,math.sqrt(3)/-3,math.sqrt(3)/-3*2,math.sqrt(3)/-3,math.sqrt(3)/3]
z_ls = [40,45,47,30,35,43,51]
G = np.c_[x_ls, y_ls, z_ls]
A = np.c_[G[:,0], G[:,1], np.ones(G.shape[0])]
C,_,_,_ = scipy.linalg.lstsq(A, G[:,2])

# regular grid covering the domain of the data
X,Y = np.meshgrid(np.arange(-3.0, 3.0, 0.5), np.arange(-3.0, 3.0, 0.5))
XX = X.flatten()
YY = Y.flatten()

Z = C[0]*X + C[1]*Y + C[2]

# plot points and fitted surface
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
ax.scatter(G[:,0], G[:,1], G[:,2], c='r', s=20)
# Hide grid lines
ax.grid(False)
# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
# plt.xlabel('X')
# plt.ylabel('Y')
# ax.set_zlabel('Z')
# ax.axis('equal')
# ax.axis('tight')
ax.set_axis_off()
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
plt.show()


