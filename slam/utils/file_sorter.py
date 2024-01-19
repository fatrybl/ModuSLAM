from pathlib import Path

from natsort import natsorted


class FileSorter:
    @staticmethod
    def sort(dir: Path, key: str) -> list:
        files = [f for f in dir.iterdir() if f.is_file()]
        if key == "name":
            return natsorted(files)
        if key == "time":
            return sorted(files, key=lambda f: f.stat().st_ctime)
        if key == "size":
            return sorted(files, key=lambda f: f.stat().st_size)
        else:
            raise Exception("Invalid key")
