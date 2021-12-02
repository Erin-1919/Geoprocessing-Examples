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





def Euclid_to_geom(*feature_fn,target_epsg=3979,cell_size=30):
    """
    Calculate Euclidean distance from each grid point to linear features.
    ---------------------------------------
    feature_fn    |    file path of the linear feature 
    target_epsg   |    EPSG code for the target CRS (default 3979)
    cell_size     |    resolution in the target CRS (default 30)
    """
    
    gdf = [geopandas.read_file(f)[['geometry']] for f in feature_fn]
    target_gdf = pandas.concat(gdf, axis=0)
    
    # reproject to target CRS
    target_gdf = target_gdf.to_crs(epsg = target_epsg)
    
    # get overall bounds of all featuresin target CRS
    bounds = target_gdf.total_bounds
    minx,miny,maxx,maxy = bounds[0],bounds[1],bounds[2],bounds[3]
    
    # create mesh grid
    ncol = round((maxx - minx)/cell_size)
    nrow = round((maxy - miny)/cell_size)
    x = numpy.linspace(minx,maxx,ncol)
    y = numpy.linspace(miny,maxy,nrow)
    X,Y = numpy.meshgrid(x,y)
    
    # create point geometry
    arr = numpy.column_stack((X.ravel(), Y.ravel()))
    df = pandas.DataFrame(arr,columns=('X','Y'))
    points_gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.X, df.Y))
    
    target = target_gdf.geometry
    points = points_gdf.geometry
    
    # calculate dist to target geometries
    dist = numpy.empty(len(points))
    
    for i, point in enumerate(points):
        dist[i] = numpy.min([numpy.min([point.distance(geom) for geom in targ]) if (targ.geom_type == 'MultiPolygon' or targ.geom_type == 'MultiLineString') else point.distance(targ) for targ in target])

    # reshape the distance matrix
    dist = dist.reshape(nrow,ncol)
    
    grid_profile = {'driver': 'GTiff', 
                    'dtype': 'float64', 
                    'nodata': -32767.0, 
                    'width': ncol, 
                    'height': nrow, 
                    'count': 1, 
                    'crs': CRS.from_epsg(target_epsg), 
                    'transform': rasterio.Affine(cell_size, 0.0, minx, 0.0, cell_size*(-1), maxy), 
                    'compress': 'lzw', 
                    'interleave': 'band'}
    
    with MemoryFile() as memfile:
        euclid_raster = memfile.open(**grid_profile)
        euclid_raster.write(dist,1)
            
        return euclid_raster


import geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
polys = world.geometry

min_dist = np.empty(n)
for i, point in enumerate(points):
    min_dist[i] = np.min([point.distance(poly) for poly in polys])
