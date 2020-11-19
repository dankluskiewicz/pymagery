import os
import sys

home_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_data_dir = os.path.join(home_dir, 'test_data')

dem_data_dir = os.path.join(test_data_dir, 'dems')
dem_paths = [os.path.join(dem_data_dir, fname) for fname in
             os.listdir(dem_data_dir)]

imagery_data_dir = os.path.join(test_data_dir, 'imagery')
imagery_paths = [os.path.join(imagery_data_dir, fname) for fname in
                 os.listdir(imagery_data_dir)]

sys.path.insert(0, home_dir)

import pymagery
