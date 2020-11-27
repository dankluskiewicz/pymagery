import pymagery
import numpy as np
import matplotlib.pyplot as plt

from . import context

crs = 'epsg:26911'
aff = np.array([1])

sb_bands = {'0': np.array([[1, 0], [0, 1]])}

mb_bands = {'1': np.array([[1, 0], [0, 1]]),
            '2': np.array([[0, 1], [1, 0]])}

rgb_bands = {'r': np.array([[1, 0], [0, 1]]),
             'g': np.array([[0, 1], [1, 0]]),
             'b': np.array([[0, 0], [1, 1]])}

raster = pymagery.Raster(bands=sb_bands)
sb = pymagery.SingleBand(bands=sb_bands)
mb = pymagery.MultiBand(bands=mb_bands)
rgb = pymagery.RGB(bands=rgb_bands)


def test_band_getitem():
    bands = pymagery.Bands({'a': 1, 'b': 2, 'c': 3})
    keyvals = [
        ('a', 1),
        ('b', 2),
        (0, 1),
        (2, 3),
        (slice(None, 2), np.array([1, 2]))
    ]
    for key, val in keyvals:
        try:
            assert bands[key] == val
        except ValueError:
            assert all(bands[key] == val)


def test_raster_init():
    raster = pymagery.Raster()


def test_single_band_init():
    pymagery.SingleBand()
    assert sb.bands == sb_bands


def test_multi_band_init():
    pymagery.MultiBand()
    assert mb.bands == mb_bands


def test_rgb_init():
    assert rgb.bands == rgb_bands
    assert list(rgb.bands.keys()) == ['r', 'g', 'b']


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
    raster.bands = mb_bands
    assert (mb_bands == raster.bands)


def test_sb_arr():
    arr = sb.arr
    print(arr)
    assert (arr == list(sb.bands.values())[0]).all()


def test_rgb_arr():
    arr = rgb.arr
    band_shape = list(rgb.bands.values())[0].shape
    assert arr.shape == (*band_shape, 3)


def test_fill_na():
    bands = {'0': np.array([[1, np.nan], [np.nan, 1]])}
    sb = pymagery.SingleBand(bands=bands)
    sb.fill_nans()
    assert all(sb.bands[0] == sb_bands[0])


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


def test_rgb_from_path():
    im_path = context.imagery_paths[0]
    rgb = pymagery.RGB.from_path(im_path)
    assert type(rgb) is pymagery.RGB
    assert list(rgb.bands.keys()) == ['r', 'g', 'b', 'a']