from phd_thesis.src.connections import EdgesFactory
from phd_thesis.src.merger import MergesFactory
from phd_thesis.src.objects import Graph
from phd_thesis.src.visualizer import visualize_graph_candidates


class CandidatesGenerator:
    @classmethod
    def create_candidates(cls, measurements: list) -> list:
        candidates = []
        vertices_combinations = MergesFactory.create_merges(measurements)
        for vertices_comb in vertices_combinations:
            edges_combinations = EdgesFactory.create_combinations(vertices_comb)
            for edges in edges_combinations:
                candidate = Graph(vertices_comb, edges)
                candidates.append(candidate)

        return candidates


measurements = [1, 2, 3, 4]
candidates = CandidatesGenerator.create_candidates(measurements)
visualize_graph_candidates(candidates)
