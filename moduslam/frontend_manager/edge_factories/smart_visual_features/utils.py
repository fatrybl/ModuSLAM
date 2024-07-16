import gtsam
import numpy as np

from moduslam.frontend_manager.edge_factories.smart_visual_features.smart_factor import (
    VisualSmartFactorFactory,
)
from moduslam.frontend_manager.edge_factories.smart_visual_features.storage import (
    VisualFeatureStorage,
)
from moduslam.frontend_manager.edge_factories.utils import find_vertex
from moduslam.frontend_manager.graph.custom_edges import SmartVisualFeature
from moduslam.frontend_manager.graph.custom_vertices import CameraPose, Feature3D, Pose
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.frontend_manager.noise_models import pixel_diagonal_noise_model
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
from moduslam.utils.auxiliary_dataclasses import VisualFeature


def get_vertex(
    storage: VertexStorage,
    timestamp: int,
    time_margin: int,
) -> CameraPose:
    """Gets vertex with the given timestamps.

    Args:
        storage: storage of vertices.

        timestamp: timestamp of the vertex.

        time_margin: time margin for the search.

    Returns:
        vertex.
    """
    cam_pose = find_vertex(CameraPose, storage, timestamp, time_margin)
    if not cam_pose:
        pose = find_vertex(Pose, storage, timestamp, time_margin)
        if pose:
            cam_pose = CameraPose(timestamp=pose.timestamp, index=pose.index, value=pose.value)
            return cam_pose
    else:
        return cam_pose

    new_index = generate_index(storage.index_storage)
    cam_pose = CameraPose(new_index, timestamp)
    return cam_pose


def create_edge(
    base_vertex: CameraPose,
    support_vertex: Feature3D,
    visual_feature: VisualFeature,
    measurement: Measurement,
    smart_factor: gtsam.SmartProjectionPose3Factor,
    noise_model: gtsam.noiseModel.Diagonal.Covariance,
) -> SmartVisualFeature:
    """Creates an edge.

    Args:
        base_vertex: optimizable vertex with camera pose.

        support_vertex: non-optimizable vertex with the visual feature position.

        visual_feature: visual feature.

        measurement: measurement with visual features.

        smart_factor: GTSAM factor.

        noise_model: GTSAM noise model.

    Returns:
        new edge.
    """
    pixels = np.array(visual_feature.key_point.pt)
    try:
        smart_factor.add(pixels, base_vertex.gtsam_index)
    except Exception:
        raise
    m = Measurement(
        time_range=measurement.time_range,
        elements=measurement.elements,
        values=visual_feature,
        handler=measurement.handler,
        noise_covariance=measurement.noise_covariance,
    )
    edge = SmartVisualFeature(base_vertex, support_vertex, m, smart_factor, noise_model)
    return edge


def create_edges(
    base_vertex: CameraPose,
    measurement: Measurement,
    feature_storage: VisualFeatureStorage,
    smart_factor_factory: VisualSmartFactorFactory,
) -> list[SmartVisualFeature]:
    """Creates an edge.

    Args:
        base_vertex: vertex with camera pose.

        measurement: measurement with visual features.

        feature_storage: storage of visual features.

        smart_factor_factory: factory to create smart factors.

    Returns:
        new edge.
    """
    sensor = measurement.elements[0].measurement.sensor
    if not isinstance(sensor, StereoCamera):
        raise TypeError(f"The sensor must be a stereo camera but got {type(sensor)!r}.")

    edges: list[SmartVisualFeature] = []
    tf = sensor.tf_base_sensor
    camera_matrix = np.array(sensor.calibrations.camera_matrix_left)
    visual_features = measurement.values
    noise_variances = (measurement.noise_covariance[0], measurement.noise_covariance[1])
    noise = pixel_diagonal_noise_model(noise_variances)

    existing_features, existing_features_indices, unique_features = feature_storage.get_features(
        visual_features
    )

    for feature, index in zip(existing_features, existing_features_indices):
        vertex, factor = feature_storage.get_vertex_and_factor(index)
        edge = create_edge(base_vertex, vertex, feature, measurement, factor, noise)
        edges.append(edge)

    for feature in unique_features:
        vertex = Feature3D(base_vertex.index, base_vertex.timestamp)
        factor = smart_factor_factory.create(tf, camera_matrix, noise)
        feature_storage.add(feature, vertex, factor)
        edge = create_edge(base_vertex, vertex, feature, measurement, factor, noise)
        edges.append(edge)

    return edges
