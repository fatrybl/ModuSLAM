from collections.abc import Iterable, Sequence


def sum_of_differences(sequence: Iterable[int], value: int) -> int:
    """Sum of absolute differences between each element and a given value.

    Args:
        sequence: A sequence of integers.

        value: The reference value for computing differences.

    Returns:
        the accumulated sum of absolute differences.
    """
    return sum(abs(item - value) for item in sequence)


def median(sequence: Sequence[int]) -> int:
    """Gets median index in the sequence based on accumulative time shift.

    Args:
        sequence: sequence to get a median in.

    Returns:
        index of the median value.
    """
    n = len(sequence)

    if n % 2 == 1:  # Odd num elements
        median_index = n // 2

    else:  # Even num elements
        median_idx_left = n // 2 - 1
        median_idx_right = n // 2
        left_median_value = sequence[median_idx_left]
        right_median_value = sequence[median_idx_right]
        total_shift_left_median = sum_of_differences(sequence, left_median_value)
        total_shift_right_median = sum_of_differences(sequence, right_median_value)

        if total_shift_left_median <= total_shift_right_median:
            median_index = median_idx_left
        else:
            median_index = median_idx_right

    return sequence[median_index]
