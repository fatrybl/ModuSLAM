import gtsam

from slam.frontend_manager.graph.edges.base_edge import Edge


class StereoCameraOdometry(Edge):
    """
    Stereo camera odometry based on images` features matching.
    """

    gtsam_factor: gtsam.BetweenFactorPose3
