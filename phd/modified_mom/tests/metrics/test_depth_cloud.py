import os

import numpy as np
import open3d as o3d
import pytest
from map_metrics.config import DepthConfig as old_depth_config
from map_metrics.metrics import mom as old_mom

from phd.modified_mom.config import DepthConfig
from phd.modified_mom.metrics import mme
from phd.modified_mom.metrics import mom as new_mom
from phd.modified_mom.metrics import mpv
from phd.modified_mom.utils import read_orthogonal_subset


@pytest.fixture
def depth_trajectories(data_dir):
    ts_folder = data_dir / "depth/poses"
    ts_names = sorted(os.listdir(ts_folder))
    trajectories = []
    for name in ts_names:
        trajectories.append(np.loadtxt(ts_folder / name, usecols=range(4)))
    return trajectories


@pytest.fixture
def depth_pointclouds(data_dir):
    pcs_folder = data_dir / "depth/pcs"
    pc_names = sorted(os.listdir(pcs_folder))
    pcs = []
    for name in pc_names:
        file_str = str(pcs_folder / name)
        pcs.append(o3d.io.read_point_cloud(file_str))
    return pcs


@pytest.fixture
def depth_orthsubset(data_dir, depth_trajectories):
    orth_list_name = str(data_dir / "depth/orth_subset/orth-0091.npy")
    orth_tj_name = str(data_dir / "depth/poses/pose-0091.txt")

    orth_list = read_orthogonal_subset(orth_list_name, orth_tj_name, depth_trajectories)

    return orth_list


@pytest.mark.parametrize(
    "config, metric, expected",
    [
        (DepthConfig, mme, -3.614438706),
        (DepthConfig, mpv, 0.003242216),
    ],
)
def test_basic_metrics(depth_pointclouds, depth_trajectories, config, metric, expected):
    actual_result = metric(pcs=depth_pointclouds, ts=depth_trajectories, config=config)
    assert abs(actual_result - expected) < 1e-3


def test_mom_new(depth_pointclouds, depth_trajectories, depth_orthsubset):
    actual_result = new_mom(
        depth_pointclouds,
        depth_trajectories,
        subsets=depth_orthsubset,
        config=DepthConfig(),
    )
    assert abs(actual_result - 0.006183082) < 1e-6


def test_mom_old(depth_pointclouds, depth_trajectories, depth_orthsubset):
    actual_result = old_mom(
        depth_pointclouds,
        depth_trajectories,
        orth_list=depth_orthsubset,
        config=old_depth_config,
    )
    assert abs(actual_result - 0.006183082) < 1e-6


def test_mom_changed(depth_pointclouds, depth_trajectories, depth_orthsubset):
    new_result = new_mom(
        depth_pointclouds,
        depth_trajectories,
        subsets=depth_orthsubset,
        config=DepthConfig(),
    )
    old_result = old_mom(
        depth_pointclouds,
        depth_trajectories,
        orth_list=depth_orthsubset,
        config=old_depth_config,
    )
    assert abs(new_result - old_result) < 1e-3
