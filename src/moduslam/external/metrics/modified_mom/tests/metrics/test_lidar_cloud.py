# import os
# from pathlib import Path
#
# import numpy as np
# import pytest
# from map_metrics.config import LidarConfig as old_lidar_config
# from map_metrics.metrics import mom as old_mom

# from src.modified_mom.config import LidarConfig
# from src.modified_mom.metrics import mom as new_mom
# from src.moduslam.map_manager.utils import read_4_channel_bin_pcd
# from src.utils.auxiliary_objects import identity4x4


# @pytest.fixture
# def lidar_pointclouds(data_dir):
#     pcs_folder = data_dir / "lidar/pcs"
#     pc_names = sorted(os.listdir(pcs_folder))
#     pcs = []
#     for name in pc_names:
#         file = pcs_folder / name
#         cloud = read_4_channel_bin_pcd(file)
#         pcs.append(cloud)
#     return pcs
#
#
# @pytest.fixture
# def small_lidar_clouds():
#     # file1 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_right/1544581170343974000.bin"
#     file2 = "/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/VLP_left/1544581170279399000.bin"
#     cloud1 = read_4_channel_bin_pcd(Path(file2))
#     return [cloud1]


# def test_mom_new(small_lidar_clouds):
#
#     new_config = LidarConfig()
#     new_config.EIGEN_SCALE = 100
#     old_config = old_lidar_config
#     old_config.MIN_CLUST_SIZE = new_config.MIN_CLUST_SIZE
#     old_config.MIN_KNN = new_config.MIN_KNN
#     old_config.MAX_NN = new_config.MAX_NN
#     old_config.KNN_RAD = new_config.KNN_RAD
#
#     i4x4 = np.asarray(identity4x4)
#
#     new_result = new_mom(
#         small_lidar_clouds,
#         [i4x4],
#         config=new_config,
#     )
#     old_result = old_mom(
#         small_lidar_clouds,
#         [i4x4],
#         config=old_config,
#     )
#     assert abs(new_result - old_result) < 1e-6
