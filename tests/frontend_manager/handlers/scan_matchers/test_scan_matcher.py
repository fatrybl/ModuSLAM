"""Tests for the Kiss ICP scan matcher.

test_process: checks if the scan matcher processes() method returns the results of the correct type
for the given elements.

TODO: either add more tests or remove unused data.
"""

from collections.abc import Iterable

from pytest import fixture, mark

from moduslam.data_manager.batch_factory.element import Element
from moduslam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from tests.frontend_manager.handlers.scan_matchers.scenarios import scenarios


@fixture
def scan_matcher() -> ScanMatcher:
    """Create a handler for test scan matching with the default configuration.

    Returns:
        ScanMatcher handler.
    """
    matcher_cfg = KissIcpScanMatcherConfig(
        name="tests_matcher",
        type_name=ScanMatcher.__name__,
        module_name="test_module",
    )
    return ScanMatcher(matcher_cfg)


@mark.parametrize("elements, reference", [*scenarios])
def test_process(
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
