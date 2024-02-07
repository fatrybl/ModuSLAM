import logging
from importlib import import_module

logger = logging.getLogger(__name__)


def as_int(value: str) -> int:
    """
    Converts value to int.
    Args:
        value (str): input value.

    Returns:
        (int): converted value.
    """
    try:
        int_value: int = int(value)
        return int_value
    except ValueError:
        msg = f"Could not convert value {value} of type {type(value)} to string"
        logger.error(msg)
        raise


def import_object(object_name: str, module_name: str, package_name: str) -> type:
    """
    Imports object with the given name.
    Args:
        object_name (str): class name.
        module_name (str): name of the module to import from.
        package_name (str): name of the package to import a module from.

    Returns:
        (type): imported object.
    """
    try:
        module = import_module(name=module_name, package=package_name)
    except ModuleNotFoundError:
        msg = f"Module {module_name!r} not found in package {package_name!r}."
        logger.error(msg)
        raise
    else:
        obj: type = getattr(module, object_name)
        return obj
