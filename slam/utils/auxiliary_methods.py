import logging


def as_int(value: str, logger: logging.Logger) -> int:
    """
    Converts value to int.
    Args:
        value (str): input value.
        logger (logging.Logger): logs errors.

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
