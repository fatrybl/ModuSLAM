"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system with Suboptimal Graph Builder.
"""

from src.logger.logging_config import LoggerConfig, setup_logger
from src.moduslam.main_manager import MainManager
from src.moduslam.setup_manager import setup_sensors

if __name__ == "__main__":
    cfg = LoggerConfig()
    cfg.level = "DEBUG"
    setup_logger(cfg)

    setup_sensors()

    manager = MainManager()

    manager.build_map()
