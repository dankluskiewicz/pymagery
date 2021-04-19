# document the areas of interest for this project
import geopandas as gpd
import shapely

bounds = (-121.6, 47.8, -121.4, 47.9)
bbox = shapely.geometry.box(*bounds)
bbox_gdf = gpd.GeoDataFrame(geometry=[bbox], crs='epsg:4326')
