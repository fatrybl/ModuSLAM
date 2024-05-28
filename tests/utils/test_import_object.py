import pytest

from moduslam.utils.auxiliary_methods import import_object


def test_import_object_valid():
    obj = import_object("OrderedSet", ".ordered_set", "moduslam.utils")
    assert obj is not None


def test_import_object_invalid_object():
    with pytest.raises(AttributeError):
        import_object("InvalidObject", ".ordered_set", "moduslam.utils")


def test_import_object_invalid_module():
    with pytest.raises(ModuleNotFoundError):
        import_object("OrderedSet", "invalid_module", "moduslam.utils")


def test_import_object_invalid_package():
    with pytest.raises(ModuleNotFoundError):
        import_object("OrderedSet", ".ordered_set", "invalid_package")
