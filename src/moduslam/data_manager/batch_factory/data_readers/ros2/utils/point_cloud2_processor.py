import numpy as np

from moduslam.custom_types.numpy import MatrixMxN

_DATATYPE_MAPPINGS = {
    1: ("int8", 1),
    2: ("uint8", 1),
    3: ("int16", 2),
    4: ("uint16", 2),
    5: ("int32", 4),
    6: ("uint32", 4),
    7: ("float32", 4),
    8: ("float64", 8),
}


def pointcloud2_to_array(msg) -> np.ndarray:
    """Converts sensor_msgs/PointCloud2 message to a structured NumPy array.

    Args:
        msg: A ROS2 sensor_msgs/PointCloud2 message.

    Returns:
        a structured NumPy array representing the point cloud.
    """
    dtype_list = []
    for field in msg.fields:
        np_dtype, _ = _DATATYPE_MAPPINGS[field.datatype]
        dtype_list.append((field.name, np_dtype))
    return np.frombuffer(msg.data, dtype=np.dtype(dtype_list))


def structured_to_regular_array(structured_array: np.ndarray) -> MatrixMxN:
    """Converts structured NumPy array to regular [N, M] float array.

    Args:
        structured_array: Structured array with named fields.

    Returns:
        a regular NumPy array of shape [N, M].
    """
    return np.stack([structured_array[name] for name in structured_array.dtype.names], axis=-1)


def filter_nans(points: MatrixMxN) -> MatrixMxN:
    """Removes rows with NaN or Inf values from point array.

    Args:
        points: Regular NumPy array of shape [N, M].

    Returns:
        a NumPy array.
    """
    return points[np.isfinite(points).all(axis=1)]
