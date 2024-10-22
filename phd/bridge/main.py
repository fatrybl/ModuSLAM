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

from phd.bridge.objects.graph_candidate import Candidate, VertexCluster
from phd.bridge.utils import create_edges_and_vertices, process_leftovers, solve
from phd.external.objects.auxiliary_objects import ClustersWithLeftovers
from phd.external.objects.measurements import Measurement
from phd.external.objects.measurements_cluster import Cluster
from phd.moduslam.frontend_manager.graph.graph import Graph

if __name__ == "__main__":

    main_graph: Graph = Graph()
    leftovers_db: list[Measurement] = []
    variants: list[list[Cluster] | ClustersWithLeftovers] = []
    errors_table: dict[Candidate, float] = {}

    for variant in variants:
        graph = deepcopy(main_graph)
        candidate = Candidate(graph)
        measurements_clusters = process_leftovers(variant, leftovers_db)

        for m_cluster in measurements_clusters:
            new_cluster = VertexCluster()

            for measurement in m_cluster.measurements:
                edges, vertices = create_edges_and_vertices(measurement, graph, candidate.clusters)
                new_cluster.vertices += vertices
                candidate.add_edges(edges)

            candidate.add_cluster(new_cluster)

        candidate.graph.add_edges(candidate.edges)
        error = solve(candidate.graph)
        errors_table.update({candidate: error})
