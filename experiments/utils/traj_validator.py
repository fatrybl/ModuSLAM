import csv
from pathlib import Path


def get_unique_sensor_names(file1: Path, file2: Path) -> dict[str, list[str]]:
    """Gets unique sensor names from two CSV files based on timestamps.

    Args:
        file1: Path to the first CSV file containing timestamp and sensor_name.
        file2: Path to the second CSV file containing timestamp and other info.

    Returns:
        A set of unique sensor names.
    """
    # Create a dictionary to map timestamps to sensor names from the first file
    timestamp_to_sensor = {}
    with file1.open("r") as f1:
        reader = csv.reader(f1, delimiter=",")
        for row in reader:
            timestamp, sensor_name = row[:2]  # Extract only the first two values
            timestamp_to_sensor[timestamp] = sensor_name.strip()

    # Create a set to store unique sensor names
    sensor_names_with_timestamps: dict[str, list[str]] = {}
    with file2.open("r") as f2:
        reader = csv.reader(f2, delimiter=",")
        for row in reader:
            timestamp = row[0]
            if timestamp in timestamp_to_sensor:
                sensor_name = timestamp_to_sensor[timestamp]
                if sensor_name not in sensor_names_with_timestamps:
                    sensor_names_with_timestamps[sensor_name] = []
                sensor_names_with_timestamps[sensor_name].append(timestamp)

    return sensor_names_with_timestamps


file1 = Path("/media/mark/WD/kaist/urban-26/sensor_data/data_stamp.csv")
file2 = Path("/final_experiments/acceleration/urban-26/output/mom_trajectory.txt")
# file2 = Path("/home/mark/Desktop/PhD/ModuSLAM/src/moduslam/trajectory.txt")
unique_sensors = get_unique_sensor_names(file1, file2)

for sensor, times in unique_sensors.items():
    print(sensor, len(times))

# 1544681687159794949
