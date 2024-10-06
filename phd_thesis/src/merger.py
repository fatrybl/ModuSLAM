from collections.abc import Iterable
from typing import Any

from phd_thesis.src.objects.cluster import Cluster
from phd_thesis.src.objects.measurements import DiscreteMeasurement


class CombinationsFactory:

    _splitter: str = "+"
    _encoder_mask: str = "item_"

    @classmethod
    def combine(cls, measurements: Iterable[DiscreteMeasurement]) -> list[list[Cluster]]:
        """Creates combinations of clusters by merging adjacent measurements.

        Args:
            measurements: measurements to create combinations of.

        Returns:
            combinations of clusters.
        """
        decoded_combinations = []
        encoded_items, mask = cls._encode_items(measurements)
        encoded_combinations = cls._create_combinations(encoded_items)

        for comb in encoded_combinations:
            decoded_comb = cls._decode_items(comb, mask)
            clusters = []
            for measurements in decoded_comb:
                cluster = Cluster()
                if isinstance(measurements, Iterable):
                    for m in measurements:
                        cluster.add(m)
                else:
                    cluster.add(measurements)

                clusters.append(cluster)

            decoded_combinations.append(clusters)

        return decoded_combinations

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
    def _encode_items(cls, items: Iterable):
        """Encodes every item as a unique string.

        Args:
            items: items to encode.

        Returns:
            encoded items.
        """
        item_to_code = {}
        code_to_item = {}

        for idx, item in enumerate(items):
            unique_code = f"{cls._encoder_mask}{idx}"
            item_to_code[item] = unique_code
            code_to_item[unique_code] = item

        return [item_to_code[item] for item in items], code_to_item

    @classmethod
    def _decode_items(cls, items: Iterable[str], mapping: dict[str, Any]) -> list:
        """Decodes items with the mapping and the splitter.

        Args:
            items: items to decode.

            mapping: a mapping table for the unique item.

        Return:
            list of decoded items.
        """
        decoded_sequence = []

        for item in items:
            if cls._splitter in item:
                parts = item.split(cls._splitter)
                decoded_parts = [mapping[part] for part in parts]
                decoded_sequence.append(decoded_parts)
            else:
                decoded_sequence.append(mapping[item])

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
    m1 = DiscreteMeasurement(1, "a")
    m2 = DiscreteMeasurement(2, "b")
    m3 = DiscreteMeasurement(3, "c")

    sequence = (m1, m2, m3)

    merges = CombinationsFactory.combine(sequence)

    for m in merges:
        print(m)
