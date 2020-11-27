import matplotlib.pyplot as plt

from . import context
import pymagery
from pymagery import utils

dem_path = context.dem_paths[0]
dem = pymagery.SingleBand.from_path(dem_path)

def test_bounding_box():
    fig, ax = plt.subplots()
    dem.plot(ax=ax)
    box = dem.bounding_box
    pymagery.utils.plot_geoms([box], ax=ax)