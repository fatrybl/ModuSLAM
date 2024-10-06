from collections.abc import Sequence


def sum_of_differences(sequence: Sequence[int], value: int) -> int:
    """Sum of absolute differences between each element and a given value.

    Args:
        sequence: A sequence of integers.

        value: The reference value for computing differences.

    Returns:
        the accumulated sum of absolute differences.

    Raises:
        ValueError: empty input sequence.
    """

    if len(sequence) == 0:
        raise ValueError("Can not compute the sum of differences of an empty sequence.")

    return sum(abs(item - value) for item in sequence)


def median(sequence: Sequence[int]) -> int:
    """Gets median value in the sequence.

    Args:
        sequence: sequence to get a median in.

    Returns:
        index of the median value.

    Raises:
        ValueError: empty input sequence.
    """
    n = len(sequence)

    if n == 0:
        raise ValueError("Can not compute the median of an empty sequence.")

    median_index = n // 2

    return sequence[median_index]
