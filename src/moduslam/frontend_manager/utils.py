from collections.abc import Iterable

from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import ContinuousImu
from src.measurement_storage.measurements.imu_bias import Bias
from src.measurement_storage.measurements.linear_velocity import Velocity
from src.measurement_storage.measurements.pose import Pose
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.measurement_storage.measurements.position import Position
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from src.moduslam.frontend_manager.main_graph.edges.base import (
    BinaryEdge,
    Edge,
    UnaryEdge,
)
from src.moduslam.frontend_manager.main_graph.edges.combined_imu_odometry import (
    ImuOdometry as CombinedImuOdometry,
)
from src.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.moduslam.frontend_manager.measurement_storage_analyzers.base import (
    StorageAnalyzer,
)
from src.utils.exceptions import NotEnoughMeasurementsError


def distribute_element(handlers: Iterable[Handler], element: Element) -> Measurement | None:
    """Processes an element with the appropriate handler.

    Args:
        handlers:

        element: element to be distributed and processed.

    Returns:
        new measurement or None.
    """
    sensor = element.measurement.sensor

    for handler in handlers:
        if handler.sensor_type == type(sensor) and handler.sensor_name == sensor.name:

            new_measurement = handler.process(element)

            if new_measurement:
                return new_measurement

            break

    return None


def fill_storage(
    storage: type[MeasurementStorage],
    data: DataBatch,
    handlers: Iterable[Handler],
    analyzer: StorageAnalyzer,
) -> None:
    """Fills the storage with the measurements created by handlers using the given data.
    The storage is filled based on the analyzer`s decision.

    Args:
        storage: a storage to fill in.

        data: a data batch with elements.

        handlers: handlers to create measurements.

        analyzer: an analyzer to decide if the storage is filled.

    Raises:
        NotEnoughMeasurementsError: not enough data to fill the storage.
    """
    enough_measurements = False

    while not enough_measurements and not data.empty:
        element = data.first
        data.remove_first()
        new_measurement = distribute_element(handlers, element)

        storage.add(new_measurement) if new_measurement else None

        enough_measurements = analyzer.check_storage(storage)
        if enough_measurements:
            return

    raise NotEnoughMeasurementsError


def get_vertices_with_measurement_timestamps(edge: Edge) -> dict[Vertex, int]:
    """Gets vertices with timestamps of measurements of the edge.

    Args:
        edge: an edge to get the measurement and the vertices of.

    Returns:
        a table of vertices with timestamps.

    Raises:
        TypeError: if the edge type is not supported.
    """

    measurement = edge.measurement
    table: dict[Vertex, int] = {}

    if isinstance(measurement, Odometry) and isinstance(edge, BinaryEdge):
        start = measurement.time_range.start
        stop = measurement.time_range.stop
        table[edge.vertex1] = start
        table[edge.vertex2] = stop

    elif isinstance(measurement, ContinuousImu) and isinstance(edge, CombinedImuOdometry):
        start = measurement.time_range.start
        stop = measurement.time_range.stop
        table[edge.pose_i] = start
        table[edge.velocity_i] = start
        table[edge.bias_i] = start
        table[edge.pose_j] = stop
        table[edge.velocity_j] = stop
        table[edge.bias_j] = stop

    elif isinstance(measurement, ContinuousImu) and isinstance(edge, ImuOdometry):
        start = measurement.time_range.start
        stop = measurement.time_range.stop
        table[edge.pose_i] = start
        table[edge.velocity_i] = start
        table[edge.bias_i] = start
        table[edge.pose_j] = stop
        table[edge.velocity_j] = stop

    elif isinstance(measurement, Pose) and isinstance(edge, UnaryEdge):
        table[edge.vertex] = measurement.timestamp

    elif isinstance(measurement, Position) and isinstance(edge, UnaryEdge):
        table[edge.vertex] = measurement.timestamp

    elif isinstance(measurement, Velocity) and isinstance(edge, UnaryEdge):
        table[edge.vertex] = measurement.timestamp

    elif isinstance(measurement, Bias) and isinstance(edge, UnaryEdge):
        table[edge.vertex] = measurement.timestamp

    else:
        raise TypeError(f"Unsupported edge type: {type(edge)}")

    return table
