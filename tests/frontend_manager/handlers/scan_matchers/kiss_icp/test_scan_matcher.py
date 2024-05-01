"""Tests for the Kiss ICP scan matcher.

test_process: checks if the scan matcher processes the elements correctly and if the result is of the correct type.
"""

from collections.abc import Iterable

from pytest import fixture, mark

from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from tests.frontend_manager.handlers.scan_matchers.kiss_icp.scenarios import scenarios


@fixture
def scan_matcher() -> ScanMatcher:
    """Create a handler for test scan matching with the default configuration.

    Returns:
        ScanMatcher handler.
    """
    matcher_cfg = KissIcpScanMatcherConfig()
    return ScanMatcher(matcher_cfg)


class TestScanMatcher:
    @mark.parametrize("elements, reference", [*scenarios])
    def test_process(
        self,
        elements: Iterable[Element],
        reference: type[Measurement] | None,
        scan_matcher: ScanMatcher,
    ) -> None:

        result: Measurement | None = None

        for element in elements:
            result = scan_matcher.process(element)

        if reference is not None:
            assert isinstance(result, reference)
        else:
            assert result is None
