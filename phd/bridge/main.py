"""На вход: список вариантов.
Вариант - список кластеров с измерениями. + остатки преинт. измерений (если есть).

Каждый вариант должен выдать список рёбер + остатки преинт. измерений (если есть).

Для каждого варианта есть копия основного графа Gt-1. G_t = Gt-1 + edges.

Базы данных вершин в Gt-1 и в DB_t должны быть одинаковые по сущности.

Берём 1-ый вариант:

1) Проверяем, есть ли неиспользованные преинт. измерения. Если да, кладём в соотв. место.
2) делаем копию основного графа G_t, создаём временную DB_t с вершинами.

3) Для каждого кластера в варианте:
    для каждого измерения в кластере:

        3.1) Создаём ребро и добавляем его в список рёбер:
            3.1.1) Создаем обязательные вершины
            3.1.2) Создаём остальные вершины
            3.1.3) Кладём новые вершины в DB_t

Создание обязательных вершин:
1) Ищем в Gt-1 последние похожие вершины, используем их значения для инициализации новых.
2) Создаем новые, используя найденные значения.
3) Создаём остальные вершины:
    для каждой вершины из остальных:
        3.1) ищем в Gt-1 + DB_t последние похожие вершины, либо проверяем их наличие в Gt-1 + DB_t.
        3.2) Создаем новые, используя найденные значения либо используем найденные  в Gt-1 + DB_t.
        3.3) Кладём новые вершины в DB_t.
"""

import logging
from copy import deepcopy

from phd.bridge.distributor import distribute
from phd.bridge.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.objects.measurements_cluster import Cluster
from phd.bridge.utils import add_elements_to_graph, process_leftovers, solve
from phd.exceptions import SkipItemException
from phd.measurements.processed_measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    graph: Graph = Graph()
    leftovers: list[Measurement] = []
    variants: list[list[Cluster] | ClustersWithLeftovers] = []
    errors_table: dict[Graph, float] = {}

    for variant in variants:
        current_graph = deepcopy(graph)
        measurements_clusters = process_leftovers(variant, leftovers)

        for m_cluster in measurements_clusters:
            current_cluster = VertexCluster()

            for measurement in m_cluster.measurements:
                edge_factory = distribute(measurement)
                try:
                    new_elements = edge_factory.create(current_graph, current_cluster, measurement)
                    add_elements_to_graph(current_graph, new_elements)

                except SkipItemException:
                    logger.warning(f"Skipping measurement:{measurement}")

        error = solve(current_graph)
        errors_table.update({current_graph: error})
