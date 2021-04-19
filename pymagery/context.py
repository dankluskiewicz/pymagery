import os

home_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_data_dir = os.path.join(home_dir, 'test_data')

dem_data_dir = os.path.join(test_data_dir, 'dems')
dem_paths = [os.path.join(dem_data_dir, fname) for fname in
             os.listdir(dem_data_dir)]

imagery_data_dir = os.path.join(test_data_dir, 'imagery')
naip_dir = os.path.join(imagery_data_dir, 'naip')
sentinel_dir = os.path.join(imagery_data_dir, 'sentinel')
naip_paths = [os.path.join(naip_dir, fname) for fname in
              os.listdir(naip_dir)]
sentinel_paths = [os.path.join(sentinel_dir, fname) for fname in
                  os.listdir(sentinel_dir)]
