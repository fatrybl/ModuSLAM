from dataclasses import dataclass


@dataclass
class BaseConfig:
    """Base Config.

    KNN_RAD: float, default=1.0
        Estimated radius between a pair of points on the map
        The value is given in meters.

    MIN_KNN: int, default=5
        Minimum number of a point neighbors.

    MAX_NN: int, default=30
        At most MAX_NN nearest neighbors that have distances to the anchor point less than a given radius.

    MIN_CLUST_SIZE: int, default=5
        Minimal acceptable cluster size in orthogonal extraction.

    MIN_NEIGHBOURS: int, default=3
        Minimal number of neighbours to calculate plane variance.

    EIGEN_SCALE: float, default=100
        Difference between 1-st and 2-nd eigen values.

    ORTHOGONALITY_EPS: float, default=1e-1
        Threshold for dot-product of 2 vectors.

    CLUSTERING_DISTANCE_TRH: float, default=1e-1
        Distance threshold for Agglomerate clustering algorithm.
    """

    KNN_RAD: float = 1.0
    MIN_KNN: int = 5
    MAX_NN: int = 20
    MIN_CLUST_SIZE: int = 5
    MIN_NEIGHBOURS: int = 3
    EIGEN_SCALE: float = 100.0
    ORTHOGONALITY_EPS: float = 1e-1
    CLUSTERING_DISTANCE_TRH: float = 1e-1


@dataclass
class DepthConfig(BaseConfig):
    """Config recommended for data obtained from Depth Camera."""

    KNN_RAD: float = 0.2
    MIN_KNN: int = 5
    MAX_NN: int = 30
    MIN_CLUST_SIZE: int = 5


@dataclass
class LidarConfig(BaseConfig):
    """Config recommended for data obtained from Lidar."""

    KNN_RAD: float = 1.5
    MIN_CLUST_SIZE: int = 10
    MAX_NN: int = 100
    MIN_KNN: int = 10
    EIGEN_SCALE: float = 20
    # KNN_RAD: float = 1.0
    # MIN_CLUST_SIZE: int = 5
    # MAX_NN: int = 30
    # MIN_KNN: int = 5
