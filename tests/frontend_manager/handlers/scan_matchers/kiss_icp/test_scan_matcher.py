from pytest import fixture, mark

from slam.data_manager.factory.element import Element
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from slam.system_configs.system.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from tests.frontend_manager.handlers.scan_matchers.kiss_icp.scenarios import scenarios


@fixture(scope="class")
def matcher() -> ScanMatcher:
    matcher_cfg = KissIcpScanMatcherConfig()
    return ScanMatcher(matcher_cfg)


class TestScanMatcher:
    """
    TODO: add more tests scenarios for KissICP Scan Matcher.
    """

    @mark.parametrize("element, reference", [*scenarios])
    def test_process(
        self, element: Element, reference: Measurement | None, matcher: ScanMatcher
    ) -> None:
        result: Measurement | None = matcher.process(element)
        assert result == reference
