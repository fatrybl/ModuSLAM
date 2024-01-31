"""
A dictionary {<sensor_name>, <handler>} to distribute different sensors` raw measurements to corresponding handlers.
"""

from slam.frontend_manager.handlers.ABC_handler import ElementHandler
from slam.frontend_manager.handlers.imu_preintegration import ImuPreintegration

sensor_handler_table: dict[str, type[ElementHandler]] = {
    "imu1": ImuPreintegration,
}
