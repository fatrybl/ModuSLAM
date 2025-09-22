"""Creates all possible combinations by merging adjacent measurement groups.

In total for N groups: sum of N-th row of Pascal triangle
or 2^(N-1) combinations.
"""

from collections import OrderedDict
from collections.abc import Iterable
from typing import TypeVar

from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.group import MeasurementGroup
from moduslam.measurement_storage.measurements.auxiliary import PseudoMeasurement

T = TypeVar("T")


class Factory:

    _splitter: str = "+"
    _encoder_mask: str = "item_"

    @classmethod
    def combine(cls, groups: Iterable[MeasurementGroup]) -> list[list[MeasurementCluster]]:
        """Creates combinations of clusters by merging adjacent measurements.

        Args:
            groups: groups of measurements with equal timestamps to create combinations of.

        Returns:
            combinations of clusters.
        """
        combinations: list[list[MeasurementCluster]] = []
        encoded_items, mask = cls._encode_items(groups)
        encoded_combinations = cls._create_combinations(encoded_items)

        for encoded_comb in encoded_combinations:
            groups_combinations = cls._decode_items(encoded_comb, mask)
            clusters = []
            for combination in groups_combinations:
                cluster = MeasurementCluster()
                for group in combination:
                    for measurement in group.measurements:
                        cluster.add(measurement)

                clusters.append(cluster)

            combinations.append(clusters)

        return combinations

    @classmethod
    def _create_combinations(cls, items: list[str]) -> list[list[str]]:
        """Creates all possible merges in deterministic order.

        Args:
            items: items to create combinations of.

        Returns:
            list of combinations in deterministic order.
        """
        if len(items) == 1:
            return [items]

        unique_results = OrderedDict[tuple[str, ...], None]()
        queue = [items]

        unique_results[tuple(items)] = None

        while queue:
            current = queue.pop(0)  # Process in FIFO order for consistency
            merged_results = cls._merge_adjacent(current)

            for merged_seq in merged_results:
                merged_tuple = tuple(merged_seq)
                if merged_tuple not in unique_results:
                    unique_results[merged_tuple] = None
                    queue.append(merged_seq)

        return [list(seq) for seq in unique_results]

    @classmethod
    def _encode_items(cls, items: Iterable[T]) -> tuple[list[str], dict[str, T]]:
        """Encodes every item as a unique string.

        Args:
            items: items to encode.
        Returns:
            encoded items and a dictionary mapping unique codes to items.
        """
        item_to_code: dict[T, str] = {}
        code_to_item: dict[str, T] = {}
        for idx, item in enumerate(items):
            unique_code = f"{cls._encoder_mask}{idx}"
            item_to_code[item] = unique_code
            code_to_item[unique_code] = item
        return [item_to_code[item] for item in items], code_to_item

    @classmethod
    def _decode_items(cls, items: Iterable[str], mapping: dict[str, T]) -> list[list[T]]:
        """Decodes items with the mapping and the splitter.
        Args:
            items: items to decode.

            mapping: a mapping table for the unique item.

        Returns:
            list of lists of decoded items.
        """
        decoded_sequence: list[list[T]] = []
        for item in items:
            if cls._splitter in item:
                parts = item.split(cls._splitter)
                decoded_parts = [mapping[part] for part in parts]
                decoded_sequence.append(decoded_parts)
            else:
                decoded_sequence.append([mapping[item]])
        return decoded_sequence

    @classmethod
    def _merge_adjacent(cls, items: list[str]) -> list[list[str]]:
        """Merges adjacent items deterministically.

        Args:
            items: items to merge.

        Returns:
            unique merges in deterministic order.
        """
        results = []
        num_items = len(items)
        for i in range(num_items - 1):
            merged = items[:i] + [f"{items[i]}{cls._splitter}{items[i + 1]}"] + items[i + 2 :]
            results.append(merged)
        return results


if __name__ == "__main__":

    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")
    m4 = PseudoMeasurement(4, "d")
    m5 = PseudoMeasurement(5, "e")
    m6 = PseudoMeasurement(6, "f")
    m7 = PseudoMeasurement(7, "g")
    m8 = PseudoMeasurement(8, "h")
    m9 = PseudoMeasurement(9, "i")

    measurements = [m1, m2, m3, m4]
    groups = [MeasurementGroup() for _ in measurements]

    for group, measurement in zip(groups, measurements):
        group.add(measurement)

    combinations = Factory.combine(groups)

    combs_dict = {}
    for c in combinations:
        num_elements = len(c)
        if num_elements not in combs_dict:
            combs_dict[num_elements] = 1
        else:
            combs_dict[num_elements] += 1

    print(combs_dict)
