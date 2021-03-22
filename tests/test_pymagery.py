import pymagery
import numpy as np
import matplotlib.pyplot as plt

from . import context


def test_band_subsetting(arr, band):
    sub_band = band[:3, :3]
    assert type(sub_band is pymagery.Band)
    assert (sub_band == arr[:3, :3]).all()


def test_band_assigment(band):
    band[0, 0] = np.nan
    assert np.isnan(band[0, 0])


def test_band_fill_na(band):
    assert False


def test_band_interp(band):
    assert False


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


def test_single_band_init(sb, sb_bands):
    pymagery.SingleBand()
    assert sb.bands == sb_bands


def test_multi_band_init(mb, mb_bands):
    pymagery.MultiBand()
    assert mb.bands == mb_bands


def test_rgb_init(rgb, rgb_bands):
    assert rgb.bands == rgb_bands
    assert list(rgb.bands.keys()) == ['r', 'g', 'b']


def test_aff(raster):
    aff = raster.aff


def test_set_aff(raster, aff):
    raster.aff = aff
    assert aff == raster.aff


def test_crs(raster):
    crs = raster.crs


def test_set_crs(raster, crs):
    raster.crs = crs


def test_set_crs_again(raster, crs):
    # should result in a warning
    # TODO: catch warning
    raster.crs = crs
    raster.crs = crs


def test_bands(raster):
    bands = raster.bands


def test_set_bands(raster, mb_bands):
    raster.bands = mb_bands
    assert (mb_bands == raster.bands)


def test_sb_arr(sb):
    arr = sb.arr
    print(arr)
    assert (arr == list(sb.bands.values())[0]).all()


def test_rgb_arr(rgb):
    arr = rgb.arr
    band_shape = list(rgb.bands.values())[0].shape
    assert arr.shape == (*band_shape, 3)


def test_fill_na(arr, sb):
    wit_nans = arr.copy()
    wit_nans[0, :3] = np.nan
    bands = {'nans': wit_nans}
    sb = pymagery.SingleBand(bands=bands)
    print(sb.arr)
    sb.fill_nans(0)
    print(sb.arr[0, :3])
    assert (sb.bands[0][0, :3] == 0).all()


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