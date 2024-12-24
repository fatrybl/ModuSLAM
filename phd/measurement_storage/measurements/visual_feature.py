from phd.measurement_storage.measurements.base import WithRawElements
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.utils.auxiliary_dataclasses import VisualFeature as FeaturePoint


class Feature(WithRawElements):
    def __init__(self, feature_point: FeaturePoint, element: Element):
        self._feature_point = feature_point
        self._element = element
        self._timestamp = element.timestamp

    @property
    def elements(self) -> list[Element]:
        return [self._element]

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def feature(self) -> FeaturePoint:
        """Detected visual feature."""
        return self._feature_point


class Features(WithRawElements):
    def __init__(self):
        raise NotImplementedError

    @property
    def elements(self) -> list[Element]:
        raise NotImplementedError

    @property
    def timestamp(self) -> int:
        raise NotImplementedError

    @property
    def features(self) -> list[Feature]:
        raise NotImplementedError
