import matplotlib.pyplot as plt

from . import context
import pymagery
from . import test_pymagery
from pymagery import utils

dem_path = context.dem_paths[0]
dem = pymagery.SingleBand.from_path(dem_path)

sb = test_pymagery.sb

def test_bounding_box():
    fig, ax = plt.subplots()
    dem.plot(ax=ax)
    box = dem.bounding_box
    # pymagery.utils.plot_geoms([box], ax=ax)
    plt.show()

def test_pix_geo_conversion():
    pix_locs = [
        (1, 1), (2, 3)
    ]
    geo_locs = [sb.pix_to_geo(i, j) for i, j in pix_locs]

    fig, ax = plt.subplots()
    sb.plot(ax=ax)
    for (i, j), (x, y) in zip(pix_locs, geo_locs):
        ax.scatter(x, y)
    plt.show()