# from pytest import fixture
# from shutil import rmtree, copytree
# from pathlib import Path
# from configs.paths.default import ConfigPaths

# CONFIGS_DIR: Path = ConfigPaths.root_path.value
# BACKUP_DIR: Path = Path(CONFIGS_DIR.as_posix() + '_backup')


# def backup():
#     copytree(CONFIGS_DIR, BACKUP_DIR)


# def clean():
#     rmtree(CONFIGS_DIR)
#     copytree(BACKUP_DIR, CONFIGS_DIR)
#     rmtree(BACKUP_DIR)


# @fixture(scope='session', autouse=True)
# def run_tests():
#     backup()
#     yield
#     clean()
