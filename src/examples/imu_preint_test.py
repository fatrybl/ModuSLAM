from pathlib import Path

import gtsam
import numpy as np
import pandas as pd

from src.bridge.edge_factories.imu_odometry.utils import (
    get_combined_integrated_measurement,
)
from src.measurement_storage.measurements.imu import (
    ContinuousImu,
    ImuCovariance,
    ImuData,
    ProcessedImu,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import ImuBias


def read_imu_data(file_path: Path, start: int, stop: int):
    column_names = [
        "timestamp",
        "quaternion x",
        "quaternion y",
        "quaternion z",
        "quaternion w",
        "Euler x",
        "Euler y",
        "Euler z",
        "Gyro x",
        "Gyro y",
        "Gyro z",
        "Acceleration x",
        "Acceleration y",
        "Acceleration z",
        "MagnetField x",
        "MagnetField y",
        "MagnetField z",
    ]

    df = pd.read_csv(file_path, header=None, names=column_names)

    columns_to_read = [
        "timestamp",
        "Gyro x",
        "Gyro y",
        "Gyro z",
        "Acceleration x",
        "Acceleration y",
        "Acceleration z",
    ]

    filtered_df = df[(df["timestamp"] >= start) & (df["timestamp"] <= stop)][columns_to_read]

    return filtered_df


def create_imu_list(filtered_df: pd.DataFrame) -> list[ProcessedImu]:
    measurements: list[ProcessedImu] = []
    tf = (
        (1.0, 0.0, 0.0, -0.07),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 1.7),
        (0.0, 0.0, 0.0, 1.0),
    )
    i3x3 = (
        (1e-3, 0.0, 0.0),
        (0.0, 1e-3, 0.0),
        (0.0, 0.0, 1e-3),
    )
    covs = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    for _, row in filtered_df.iterrows():
        velocity = (row["Gyro x"], row["Gyro y"], row["Gyro z"])
        accel = (row["Acceleration x"], row["Acceleration y"], row["Acceleration z"])
        data = ImuData(velocity, accel)
        m = ProcessedImu(row["timestamp"], data, covs, tf)
        measurements.append(m)
    return measurements


if __name__ == "__main__":
    file_path = Path("/media/mark/New Volume/datasets/kaist/urban-26/sensor_data/xsens_imu.csv")
    start = 1544581170281231410
    stop = 1544581171187127000
    filtered_data = read_imu_data(file_path, start, stop)

    timescale: float = 1e-9
    params = gtsam.PreintegrationCombinedParams.MakeSharedU(9.81)
    imu_list = create_imu_list(filtered_data)
    continuous = ContinuousImu(imu_list, start, stop)
    bias = ImuBias(0)
    pim = get_combined_integrated_measurement(params, continuous, stop, timescale, bias)

    state = gtsam.NavState()
    gyro_b = np.array((0.1, 0.1, 0.1))
    accel_b = np.array((0.1, 0.1, 0.1))
    b = gtsam.imuBias.ConstantBias(gyro_b, accel_b)
    pim1 = gtsam.PreintegratedCombinedMeasurements(params, b)
    print(pim.predict(state, b))
    print(pim.deltaPij())
