import pymagery
import os
import numpy as np
import matplotlib.pyplot as plt

from . import context

raster = pymagery.Raster()
sb = pymagery.SingleBand()
mb = pymagery.MultiBand()


def test_raster_plot():
    fig, ax = raster.plot()
    ax.set_title('test default raster plot')
    plt.show


def test_single_band_plot():
    fig, ax = sb.plot()
    ax.set_title('test default sb plot')
    plt.show()


def test_sb_from_path():
    dem_path = context.dem_paths[0]
    sb = pymagery.Raster.from_path(dem_path)
    fig, ax = sb.plot()
    ax.set_title('test dem sb raster plot')
    plt.show()
