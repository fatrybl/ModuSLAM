from collections.abc import Iterable
from typing import TypeVar

from phd.measurements.auxiliary_classes import MeasurementGroup, PseudoMeasurement
from phd.measurements.cluster import Cluster

T = TypeVar("T")


class Factory:

    _splitter: str = "+"
    _encoder_mask: str = "item_"

    @classmethod
    def combine(cls, groups: Iterable[MeasurementGroup]) -> list[list[Cluster]]:
        """Creates combinations of clusters by merging adjacent measurements.

        Args:
            groups: groups of measurements with equal timestamps to create combinations of.

        Returns:
            combinations of clusters.
        """
        combinations: list[list[Cluster]] = []
        encoded_items, mask = cls._encode_items(groups)
        encoded_combinations = cls._create_combinations(encoded_items)

        for encoded_comb in encoded_combinations:
            groups_combinations = cls._decode_items(encoded_comb, mask)
            clusters = []
            for combination in groups_combinations:
                cluster = Cluster()
                for group in combination:
                    for measurement in group.measurements:
                        cluster.add(measurement)

                clusters.append(cluster)

            combinations.append(clusters)

        return combinations

    @classmethod
    def _create_combinations(cls, items: list[str]) -> list[list[str]]:
        """Creates all possible merges.

        Args:
            items: items to create combinations of.

        Returns:
            list of combinations.
        """

        if len(items) == 1:
            return [items]

        unique_results = set()
        queue = [items]

        unique_results.add(tuple(items))

        while queue:
            current = queue.pop()
            merged_results = cls._merge_adjacent(current)
            unique_results.update(merged_results)

            for merged_seq in merged_results:
                if len(merged_seq) > 1:  # Continue merging if more than one element
                    queue.append(list(merged_seq))

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
    def _merge_adjacent(cls, items: list[str]) -> set[tuple[str, ...]]:
        """Merges adjacent items.

        Args:
            items: items to merge.

        Returns:
            unique merges.
        """
        results = set()
        num_items = len(items)
        for i in range(num_items - 1):
            merged = items[:i] + [f"{items[i]}{cls._splitter}{items[i + 1]}"] + items[i + 2 :]
            results.add(tuple(merged))  # Use tuple to store in a set
        return results


if __name__ == "__main__":
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")

    g1, g2, g3 = MeasurementGroup(), MeasurementGroup(), MeasurementGroup()

    g1.add(m1)
    g2.add(m2)
    g3.add(m3)

    sequence = (g1, g2, g3)

    combinations = Factory.combine(sequence)

    for c in combinations:
        print(c)
