import requests
import json 

## search by bbox

#STAC API search endpoint
url = "https://datacube.services.geo.ca/api/search?collections=cdem&bbox=-127.108488,60.816433,-117.151858,65.027262"

#POST request adding the defined payload
response = requests.request("GET", url)

#Loads response as JSON
json_object = json.loads(response.text)

#Format JSON for printing
json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)

## search by ids

url = "https://datacube.services.geo.ca/api/search?collections=cdem&ids=cdem-1"
response = requests.request("GET", url)
json_object = json.loads(response.text)
json_formatted_str = json.dumps(json_object, indent=2)
print(json_formatted_str)

## search by datetime
url = "https://datacube.services.geo.ca/api/search?collections=cdem&datetime=1978-01-01T00:00:00Z"
response = requests.request("GET", url)
json_object = json.loads(response.text)
json_formatted_str = json.dumps(json_object, indent=2)
print(json_formatted_str)

## get by ids

url = "https://datacube.services.geo.ca/api/collections/cdem/items/cdem-1"
response = requests.request("GET", url)
json_object = json.loads(response.text)
json_formatted_str = json.dumps(json_object, indent=2)
print(json_formatted_str)

##  display the poligons of the coverages over a map 

from shapely.geometry import shape
from shapely.ops import unary_union
from ipyleaflet import Map, basemaps, GeoData
from geopandas import GeoDataFrame

#Initialize list to contain coverages' bounding boxes
bboxes=[]

#Loop through the coverages returned
for feature in json_object['features']: #
    #Get the polygon as a string from the JSON geometry field of the coverages
    cdem=feature['geometry']
    #Translate into a shapely geometry
    geom = shape(cdem)
    #Append the bounding box to the list
    bboxes.append(geom)
    
#Create a Multipolygon combining all the bounding boxes to properly calculate the centroid of the geometries
polygons = unary_union(bboxes)

# Define the center of the map as the polygons' centroid
center = (polygons.centroid.y, polygons.centroid.x)

# Generate map
m2 = Map(center=center,zoom = 3, projection="EPSG4326", basemap= basemaps.Esri.WorldTopoMap)
    
for bbox in bboxes:
    #Generate a layer for each bbox and add it to the map
    bboxData = GeoDataFrame()
    bboxData['geometry'] = None
    bboxData.loc[0, 'geometry'] = bbox
    bboxData.crs = "EPSG:4326"
    geo_data = GeoData(geo_dataframe = bboxData,
                       name = 'BBox')
    m2.add_layer(geo_data)

#Display map
m2

## search by bbox