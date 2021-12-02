import matplotlib.pyplot as plt
import shapely.geometry as geom
import numpy as np
import pandas as pd
import geopandas as gpd

lines = gpd.GeoSeries(
    [geom.LineString(((1.4, 3), (0, 0))),
        geom.LineString(((1.1, 2.), (0.1, 0.4))),
        geom.LineString(((-0.1, 3.), (1, 2.)))])

# 10 points
n  = 10
points = gpd.GeoSeries([geom.Point(x, y) for x, y in np.random.uniform(0, 3, (n, 2))])

# Put the points in a dataframe, with some other random column
df_points = gpd.GeoDataFrame(np.array([points, np.random.randn(n)]).T)
df_points.columns = ['Geometry', 'Property1']

min_dist = np.empty(n)
for i, point in enumerate(points):
    min_dist[i] = np.min([point.distance(line) for line in lines])
df_points['min_dist_to_lines'] = min_dist
df_points.head(3)

def min_distance(point, lines):
    return lines.distance(point).min()

df_points['min_dist_to_lines'] = df_points.geometry.apply(min_distance, df_lines)
# df_points['min_dist_to_lines'] = df_points.geometry.apply(min_distance, args=(df_lines,))


# https://stackoverflow.com/questions/30740046/calculate-distance-to-nearest-feature-with-geopandas



import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
polys = world.geometry

min_dist = np.empty(n)
for i, point in enumerate(points):
    min_dist[i] = np.min([point.distance(poly) for poly in polys])