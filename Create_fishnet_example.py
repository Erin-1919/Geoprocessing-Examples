import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

points = gpd.read_file('Data/study_area.shp')

xmin, ymin, xmax, ymax = points.total_bounds

length = (xmax-xmin)/5
wide = (ymax-ymin)/5

cols = list(np.arange(xmin, xmax + wide, wide))
rows = list(np.arange(ymin, ymax + length, length))

polygons = []
for x in cols[:-1]:
    for y in rows[:-1]:
        polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))

grid = gpd.GeoDataFrame({'geometry':polygons})
grid.to_file('test.shp')