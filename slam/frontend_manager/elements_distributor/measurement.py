from dataclasses import dataclass
from typing import Any, Type

from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.handlers.ABC_module import ElementHandler
from slam.utils.auxiliary_dataclasses import TimeRange


@dataclass
class Measurement:
    """
    A measurement obtained from the preprocessed element(s)
    """
    time_range: TimeRange
    value: Any
    type: Type[ElementHandler]
    elements: tuple[Element]
