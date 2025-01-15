from dataclasses import dataclass


@dataclass
class BaseConfig:
    """Base Config.

    knn_rad: float, default=1.0
        Estimated radius between a pair of points on the map
        The value is given in meters.

    min_knn: int, default=5
        Minimum number of a point neighbors.

    max_nn: int, default=30
        At most MAX_NN nearest neighbors that have distances to the anchor point less than a given radius.

    min_cluster_size: int, default=5
        Minimal acceptable cluster size in orthogonal extraction.

    min_neighbours: int, default=3
        Minimal number of neighbours to calculate plane variance.

    eigen_scale: float, default=100
        Difference between 1-st and 2-nd eigen values.

    orthogonality_trh: float, default=1e-1
        Threshold for dot-product of 2 vectors.
    """

    knn_rad: float = 1.0
    min_knn: int = 5
    max_nn: int = 20
    min_cluster_size: int = 5
    min_neighbours: int = 3
    eigen_scale: float = 100.0
    orthogonality_trh: float = 1e-1


@dataclass
class DepthConfig(BaseConfig):
    """Config recommended for data obtained from Depth Camera."""

    knn_rad: float = 0.2
    min_knn: int = 5
    max_nn: int = 30
    min_cluster_size: int = 5


@dataclass
class LidarConfig(BaseConfig):
    """Config recommended for data obtained from Lidar."""

    knn_rad: float = 1.5
    min_cluster_size: int = 10
    max_nn: int = 100
    min_knn: int = 10
    eigen_scale: float = 20


@dataclass
class HdbscanConfig:
    """Config for HDBSCAN clustering algorithm.

    min_cluster_size: int, default=10
        The minimum size of clusters.

    n_jobs: int, default=-1
        The number of parallel jobs to run.

    alpha: float, default=1.5
        The alpha value for HDBSCAN clustering.

    cluster_selection_epsilon: float, default=0.2
        The epsilon value for HDBSCAN clustering.
    """

    n_jobs: int = -1
    alpha: float = 1.5
    cluster_selection_epsilon: float = 0.2
