import numpy as np
import open3d as o3d


def visualize_pointcloud(pointcloud: o3d.geometry.PointCloud):
    """Visualize a point cloud using open3d library.

    Args:
        pointcloud (o3d.geometry.PointCloud): The point cloud object to visualize.
    """

    o3d.visualization.draw_geometries([pointcloud])


def pointcloud_to_file(
    file_name: str,
    pointcloud_data: np.ndarray,
    file_format: str = "auto",
    write_ascii: bool = False,
    compress: bool = False,
    print_progress: bool = True,
) -> None:
    """Save a numpy array of shape Nx4 with points [x, y, z, intensity] to a point cloud
    file using open3d.

    Args:
        file_name (str): The name of the file to save the point cloud to.
        pointcloud_data (np.ndarray): A numpy array of shape Nx4 with points [x, y, z, intensity].
        file_format (str): The format of the file to save the point cloud to. Default is "auto".
        print_progress (bool): Print progress bar.
        compress (bool): Compress the file.
        write_ascii (bool): Write the file in ASCII format.
    """
    dimensions: int = 3
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pointcloud_data[:, :dimensions])
    o3d.io.write_point_cloud(
        file_name,
        pcd,
        format=file_format,
        write_ascii=write_ascii,
        compressed=compress,
        print_progress=print_progress,
    )


def pointcloud_from_file(
    file_name: str,
    file_format: str | None = "auto",
    remove_nan: bool = True,
    remove_infinity: bool = True,
    print_progress: bool = True,
) -> o3d.geometry.PointCloud:
    """Read a point cloud from a binary file using open3d.

    Args:
        file_name (str): The name of the file to read the point cloud from.
        file_format (str): The format of the file to read the point cloud from.
                If None, the format is inferred from the file extension.
        remove_nan (bool): Remove NaN points.
        remove_infinity (bool): Remove infinite points.
        print_progress (bool): Print progress bar.


    Returns:
        o3d.geometry.PointCloud: The point cloud object.
    """
    pcd = o3d.io.read_point_cloud(
        file_name,
        format=file_format,
        print_progress=print_progress,
        remove_nan_points=remove_nan,
        remove_infinite_points=remove_infinity,
    )

    return pcd
