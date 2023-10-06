import logging


def as_int(value: str, logger: logging.Logger) -> int:
    try:
        value = int(value)
    except ValueError:
        msg = f"Could not convert value {value} of type {type(value)} to string"
        logger.error(msg)
        raise
    else:
        return value
