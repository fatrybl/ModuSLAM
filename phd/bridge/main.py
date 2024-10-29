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

from copy import deepcopy

from phd.bridge.utils import create_graph_elements, process_leftovers, solve
from phd.external.objects.auxiliary_objects import ClustersWithLeftovers
from phd.external.objects.measurements import Measurement
from phd.external.objects.measurements_cluster import Cluster as MeasurementCluster
from phd.moduslam.frontend_manager.main_graph.graph import Graph

if __name__ == "__main__":

    graph: Graph = Graph()
    leftovers_db: list[Measurement] = []
    variants: list[list[MeasurementCluster] | ClustersWithLeftovers] = []
    errors_table: dict[Graph, float] = {}

    for variant in variants:
        current_graph = deepcopy(graph)
        measurements_clusters = process_leftovers(variant, leftovers_db)

        for cluster in measurements_clusters:
            for measurement in cluster.measurements:

                new_elements = create_graph_elements(measurement, current_graph)

                for element in new_elements:
                    current_graph.add_element(element)

        error = solve(current_graph)
        errors_table.update({current_graph: error})
