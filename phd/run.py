"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system with Suboptimal Graph Builder.
"""

from phd.logger.logging_config import LoggerConfig, setup_logger
from phd.moduslam.main_manager.manager import MainManager

if __name__ == "__main__":
    cfg = LoggerConfig()
    cfg.level = "DEBUG"
    setup_logger(cfg)

    manager = MainManager()
    manager.build_map()
