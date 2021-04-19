import geopandas as gpd
import folium


def plot_geoms(geoms, ax,
               edgecolor='k', facecolor='none', **plotting_kwargs):
    """
    plot a shapely polygon
    """
    gdf = gpd.GeoDataFrame(geometry=geoms)
    gdf.plot(ax=ax, edgecolor=edgecolor, facecolor=facecolor,
             **plotting_kwargs)


# default style params for show_polys
dflt_style = {
    'fillColor': 'orange',
    'color': 'k',
    'weight': '3',
    'opacity': '1',
    'fillOpacity': '.2',
}


def show_gdf(gdf, m=None, popup=None, tooltip=None, style_function=None):
    """
    plot a geodataframe in an interactive map
    """
    center = gdf.to_crs('epsg:4326').geometry.centroid.unary_union.centroid

    if m is None:
        bkgrnd_tiles = ('https://server.arcgisonline.com/ArcGIS/rest/'
                        'services/World_Imagery/MapServer/tile/{z}/{y}/{x}')
        attr = ('Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, '
                'AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and '
                'the GIS User Community', )

        m = folium.Map(location=(center.y, center.x), zoom_start=12,
                       tiles=bkgrnd_tiles, attr=attr)

    if type(popup) is str:
        popup = folium.features.GeoJsonPopup(
            fields=[popup],
            localize=True,
            labels=True,
            style="background-color: yellow;",
        )
    if type(tooltip) is str:
        tooltip = folium.features.GeoJsonTooltip(
            fields=[tooltip],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )
    if style_function is None:
        def style_function(x):
            return dflt_style

    folium.GeoJson(gdf, popup=popup,
                   tooltip=tooltip,
                   style_function=style_function).add_to(m)
    return m
