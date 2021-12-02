import geopandas as gpd
import rasterio
from rasterio import features

# Set up your filenames
shp_fn = 'cb_2013_us_county_20m.shp'
rst_fn = 'template_raster.tif'
out_fn = './rasterized.tif'

# Open the file with GeoPANDAS read_file
counties = gpd.read_file(shp_fn)

# Add the new column (as in your above code)
for i in range (len(counties)):
    LSAD = counties.at[i,'LSAD']
    if LSAD == 00 :
        counties['LSAD_NUM'] == 'A'
    elif LSAD == 3 :
        counties['LSAD_NUM'] == 'B'
    elif LSAD == 4 :
        counties['LSAD_NUM'] == 'C'
    elif LSAD == 5 :
        counties['LSAD_NUM'] == 'D'
    elif LSAD == 6 :
        counties['LSAD_NUM'] == 'E'
    elif LSAD == 13 :
        counties['LSAD_NUM'] == 'F'
    elif LSAD == 15 :
        counties['LSAD_NUM'] == 'G'  
    elif LSAD == 25 :
        counties['LSAD_NUM'] == 'I'          
    else :
        counties['LSAD_NUM'] == 'NA'
        
# Open the raster file you want to use as a template for feature burning using rasterio
rst = rasterio.open(rst_fn)

# copy and update the metadata from the input raster for the output
meta = rst.meta.copy()
meta.update(compress='lzw')

# Now burn the features into the raster and write it out
with rasterio.open(out_fn, 'w+', **meta) as out:
    out_arr = out.read(1)

    # this is where we create a generator of geom, value pairs to use in rasterizing
    shapes = ((geom,value) for geom, value in zip(counties.geometry, counties.LSAD_NUM))

    burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
    out.write_band(1, burned)