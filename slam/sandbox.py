
from typing import Iterable
from collections.abc import Iterator, Callable
from slam.utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


def init_iterator(data: Iterable[float]) -> Iterator[float]:
    for element in data:
        yield element


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    iter = init_iterator(test)
    iter2 = iter

    print(next(iter))
    print(next(iter))
    print(next(iter))
    iter = init_iterator(test)
    print(next(iter))
    print('asdasdasdasdas')
    print(next(iter))
    print(next(iter2))
    print(next(iter2))
