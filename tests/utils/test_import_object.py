import pytest

from slam.utils.auxiliary_methods import import_object


def test_import_object_valid():
    obj = import_object("OrderedSet", ".ordered_set", "slam.utils")
    assert obj is not None


def test_import_object_invalid_object():
    with pytest.raises(AttributeError):
        import_object("InvalidObject", ".ordered_set", "slam.utils")


def test_import_object_invalid_module():
    with pytest.raises(ModuleNotFoundError):
        import_object("OrderedSet", "invalid_module", "slam.utils")


def test_import_object_invalid_package():
    with pytest.raises(ModuleNotFoundError):
        import_object("OrderedSet", ".ordered_set", "invalid_package")
