import numpy as np

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


def pointcloud2_to_array(msg):
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


def structured_to_regular_array(struct_array):
    """Converts structured NumPy array to regular [N, M] float array.

    Args:
        struct_array: Structured array with named fields.

    Returns:
        a regular NumPy array of shape [N, M].
    """
    return np.stack([struct_array[name] for name in struct_array.dtype.names], axis=-1)


def filter_nans(points):
    """Removes rows with NaN or Inf values from point array.

    Args:
        points: Regular NumPy array of shape [N, M].

    Returns:
        a NumPy array.
    """
    return points[np.isfinite(points).all(axis=1)]
