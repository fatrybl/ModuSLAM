from ast import main
from source.main_manager import MainManager

"""
Author: Mark Griguletskii.

Main runner of the mapping system.
"""

def run():
    main_manager = MainManager()
    main_manager.setup_system()
    main_manager.build_map()

if __name__ == "__main__":
    run()