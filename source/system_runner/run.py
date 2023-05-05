from src.main_manager import MainManager
# SetupManager, DataManager, FrontendManager, BackendManager, MapManager

"""
Author: Mark Griguletskii.

Main runner of the mapping system.
"""

def run():
    main_manager = MainManager()
    main_manager.build_map()

if __name__ == "__main__":
    run()