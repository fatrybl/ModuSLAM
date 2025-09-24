from collections.abc import Iterable
from typing import Any

from moduslam.bridge.auxiliary_dataclasses import Connection
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import PseudoMeasurement


class Factory:

    _encoder_mask: str = "item_"
    _splitter_1: str = "+"
    _splitter_2: str = ","

    @classmethod
    def create_combinations(cls, clusters: list[MeasurementCluster]) -> list[list[Connection]]:
        """Creates combinations of connections.

        Args:
            clusters: clusters to create combinations of connections for.

        Returns:
            combinations.
        """
        if len(clusters) == 1:
            return []

        combinations = []
        encoded_clusters, mask = cls._encode_items(clusters)
        connections = cls._create_connections(encoded_clusters)
        for con in connections:
            combination = []
            decoded_con = cls._decode_items(con, mask)
            for pair in decoded_con:
                connection = Connection(pair[0], pair[1])
                combination.append(connection)

            combinations.append(combination)

        return combinations

    @classmethod
    def _create_connections(cls, items: list):
        """Creates all possible connections between items without intersections.

        Args:
            items: items to connect.

        Returns:
            connections.

        TODO: remove sorting after debugging to speed up the process.
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
        return sorted(results)

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


if __name__ == "__main__":
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")
    c1 = MeasurementCluster()
    c2 = MeasurementCluster()
    c3 = MeasurementCluster()

    c1.add(m1)
    c2.add(m2)
    c3.add(m3)

    sequence = [c1, c2, c3]
    edges_combinations = Factory.create_combinations(sequence)

    for comb in edges_combinations:
        print(comb)
