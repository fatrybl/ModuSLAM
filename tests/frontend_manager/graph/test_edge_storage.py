"""Tests for EdgeStorage class."""

import pytest
from gtsam import PriorFactorPoint2
from gtsam.noiseModel import Diagonal

from slam.frontend_manager.graph.base_edges import BinaryEdge, MultiEdge, UnaryEdge
from slam.frontend_manager.graph.edge_storage import EdgeStorage
from tests.frontend_manager.conftest import BasicTestVertex


@pytest.fixture
def edge_storage() -> EdgeStorage:
    return EdgeStorage[BinaryEdge | UnaryEdge | MultiEdge]()


class TestEdgeStorage:

    vertex1 = BasicTestVertex()
    vertex2 = BasicTestVertex()
    vertex3 = BasicTestVertex()

    edge1 = BinaryEdge(
        vertex1,
        vertex2,
        measurements=(),
        noise_model=Diagonal.Sigmas([1, 1]),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Diagonal.Sigmas([1, 1])),
    )

    edge2 = UnaryEdge(
        vertex1,
        measurements=(),
        noise_model=Diagonal.Sigmas([1, 1]),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Diagonal.Sigmas([1, 1])),
    )

    edge3 = UnaryEdge(
        vertex3,
        measurements=(),
        noise_model=Diagonal.Sigmas([1, 1]),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Diagonal.Sigmas([1, 1])),
    )

    edge4 = MultiEdge(
        vertex_set_1={vertex1, vertex2},
        vertex_set_2={vertex3},
        measurements=(),
        noise_model=Diagonal.Sigmas([1, 1]),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Diagonal.Sigmas([1, 1])),
    )

    def test_add(self, edge_storage):

        edge_storage.add(self.edge1)
        assert self.edge1 in edge_storage._edges

        edge_storage.add([self.edge2, self.edge4])
        assert self.edge2 in edge_storage._edges
        assert self.edge4 in edge_storage._edges

    def test_add_multiple(self, edge_storage):

        edge_storage.add([self.edge1, self.edge2, self.edge3, self.edge4])
        assert self.edge1 in edge_storage._edges
        assert self.edge2 in edge_storage._edges
        assert self.edge3 in edge_storage._edges
        assert self.edge4 in edge_storage._edges

    def test_remove(self, edge_storage):

        edge_storage.add(self.edge1)
        edge_storage.remove(self.edge1)
        assert self.edge1 not in edge_storage._edges

        edge_storage.add([self.edge2, self.edge3])
        edge_storage.remove([self.edge2, self.edge3])
        assert self.edge2 not in edge_storage._edges
        assert self.edge3 not in edge_storage._edges

    def test_remove_multiple(self, edge_storage):

        edge_storage.add([self.edge1, self.edge2, self.edge3, self.edge4])
        edge_storage.remove([self.edge1, self.edge2, self.edge3, self.edge4])
        assert self.edge1 not in edge_storage._edges
        assert self.edge2 not in edge_storage._edges
        assert self.edge3 not in edge_storage._edges
        assert self.edge4 not in edge_storage._edges
        assert len(edge_storage.edges) == 0
