import geopandas as gpd


def plot_geoms(geoms, ax,
               edgecolor='k', facecolor='none', **plotting_kwargs):
    """
    plot a shapely polygon
    """
    gdf = gpd.GeoDataFrame(geometry=geoms)
    gdf.plot(ax=ax, edgecolor=edgecolor, facecolor=facecolor, **plotting_kwargs)
