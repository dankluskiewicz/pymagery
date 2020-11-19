import pymagery
import numpy as np
import matplotlib.pyplot as plt

from . import context

crs = 'epsg:26911'
aff = np.array([1])
bands = {'test_band': np.zeros([3, 5, 6])}
raster = pymagery.Raster()
sb = pymagery.SingleBand()
mb = pymagery.MultiBand()

def test_raster_init():
    raster = pymagery.Raster()

def test_single_band_init():
    sb = pymagery.SingleBand()
    assert sb.bands == pymagery.SingleBand.dflt_bands

def test_multi_band_init():
    mb = pymagery.MultiBand()
    assert mb.bands == pymagery.MultiBand.dflt_bands

def test_aff():
    aff = raster.aff

def test_set_aff():
    raster.aff = aff
    assert all(aff == raster.aff)

def test_crs():
    crs = raster.crs

def test_set_crs():
    raster.crs = crs

def test_set_crs_again():
    # should result in a warning
    # TODO: catch warning
    raster.crs = crs
    raster.crs = crs

def test_bands():
    bands = raster.bands

def test_set_bands():
    raster.bands = bands
    assert (bands == raster.bands)

def test_sb_from_path():
    dem_path = context.dem_paths[0]
    sb = pymagery.Raster.from_path(dem_path)
    assert type(sb) is pymagery.SingleBand
    assert sb.aff is not None
    assert sb.crs is not None

def test_mb_from_path():
    im_path = context.imagery_paths[0]
    mb = pymagery.Raster.from_path(im_path)
    assert type(mb) is pymagery.MultiBand
    assert mb.aff is not None
    assert mb.crs is not None