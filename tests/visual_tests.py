import matplotlib.pyplot as plt

import pymagery
from pymagery import utils


def test_bounding_box(dem):
    box = dem.bounding_box
    fig, ax = plt.subplots()
    dem.plot(ax=ax)
    pymagery.utils.plot_geoms([box], ax=ax, linewidth=5)
    plt.show()


def test_pix_geo_conversion(sb):
    pix_locs = [
        (1, 1), (2, 3)
    ]
    print(type(sb))
    print(sb.aff)
    geo_locs = [sb.pix_to_geo(i, j) for i, j in pix_locs]

    fig, ax = plt.subplots()
    sb.plot(ax=ax)
    for (i, j), (x, y) in zip(pix_locs, geo_locs):
        ax.scatter(x, y)
    plt.show()
