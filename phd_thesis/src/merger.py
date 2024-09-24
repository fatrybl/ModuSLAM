from collections.abc import Iterable
from typing import Any

from phd_thesis.src.objects import Vertex


class MergesFactory:

    _splitter: str = "+"
    _encoder_mask: str = "item_"

    @classmethod
    def create_merges(cls, items: list) -> list[list]:
        """Creates all possible combinations by merging adjacent items.

        Args:
            items: items to create combinations of.

        Returns:
            list of combinations.
        """
        decoded_combinations = []
        encoded_items, mask = cls._encode_items(items)
        encoded_combinations = cls._create_combinations(encoded_items)

        for comb in encoded_combinations:
            decoded_comb = cls._decode_items(comb, mask)
            vertices = []
            for measurements in decoded_comb:
                if isinstance(measurements, Iterable):
                    vertex = Vertex(tuple(measurements))
                else:
                    vertex = Vertex((measurements,))
                vertices.append(vertex)

            decoded_combinations.append(vertices)

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
        for i in range(len(items) - 1):
            merged = items[:i] + [f"{items[i]}{cls._splitter}{items[i + 1]}"] + items[i + 2 :]
            results.add(tuple(merged))  # Use tuple to store in a set
        return results


# sequence = [1, 2, 3]
#
# merges = MergesFactory.create_merges(sequence)
#
# for m in merges:
#     print(m)
