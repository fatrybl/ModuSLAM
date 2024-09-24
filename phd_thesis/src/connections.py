from collections.abc import Iterable
from typing import Any

from phd_thesis.src.objects import Edge, Vertex


class EdgesFactory:

    _encoder_mask: str = "item_"
    _splitter_1: str = "+"
    _splitter_2: str = ","

    @classmethod
    def create_combinations(cls, vertices: list[Vertex]) -> list[list[Edge]]:
        """Creates all edges combinations.

        Args:
            vertices: vertices to create edges connections for.

        Returns:
            edges combinations.
        """
        if len(vertices) == 1:
            return []

        combinations = []
        encoded_vertices, mask = cls._encode_items(vertices)
        connections = cls._create_connections(encoded_vertices)
        for con in connections:
            edges = []
            decoded_con = cls._decode_items(con, mask)
            for pair in decoded_con:
                edge = Edge(pair[0], pair[1])
                edges.append(edge)

            combinations.append(edges)

        return combinations

    @classmethod
    def _create_connections(cls, items: list):
        """Creates all possible connections between vertices.

        Args:
            items: vertices to connect.

        Returns:
            list of connections.
        """
        n = len(items)
        if n <= 1:
            return []

        total_steps = n - 1
        compositions = cls._generate_compositions(total_steps)
        results = []
        for composition in compositions:
            edges = []
            current_vertex_index = 0
            for step in composition:
                next_vertex_index = current_vertex_index + step
                if next_vertex_index >= n:
                    break  # Avoid index out of range
                v1 = items[current_vertex_index]
                v2 = items[next_vertex_index]
                edges.append(f"{v1}{cls._splitter_1}{v2}")
                current_vertex_index = next_vertex_index
            else:
                # Only add the result if we have connected to the last vertex
                if current_vertex_index == n - 1:
                    result = cls._splitter_2.join(edges)
                    results.append(f"{result}")
        # Remove duplicates
        results = list(set(results))
        return results

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
    def _decode_items(cls, input_str: str, mapping: dict[str, Any]) -> list[list[Any]]:
        """Decodes string values with the mapping.

        Args:
            input_str: string with values

            mapping: "string->value" mapping.

        Returns:
            pairs with values.
        """
        pairs = input_str.split(cls._splitter_2)
        items = [pair.split(cls._splitter_1) for pair in pairs]
        mapped_items = [[mapping[value] for value in item] for item in items]
        return mapped_items

    @classmethod
    def _generate_compositions(cls, n: int) -> list[list[int]]:
        """Generates all possible compositions (partitions).

        Args:
            n: integer value.

        Returns
            compositions.
        """
        if n == 0:
            return [[]]
        compositions = []
        for i in range(1, n + 1):
            for tail in cls._generate_compositions(n - i):
                compositions.append([i] + tail)
        return compositions


# v1 = Vertex(1)
# v2 = Vertex(2)
# v3 = Vertex(3)
#
# sequence = [v1, v2, v3]
# edges_combinations = EdgesFactory.create_combinations(sequence)
#
# for comb in edges_combinations:
#     print(comb)
