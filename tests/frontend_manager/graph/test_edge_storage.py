"""Tests for EdgeStorage class."""

import pytest
from gtsam import PriorFactorPoint2
from gtsam.noiseModel import Isotropic

from moduslam.frontend_manager.graph.base_edges import BinaryEdge, MultiEdge, UnaryEdge
from moduslam.frontend_manager.graph.edge_storage import EdgeStorage
from tests.frontend_manager.conftest import measurement
from tests.frontend_manager.objects import BasicTestVertex


@pytest.fixture
def edge_storage() -> EdgeStorage:
    return EdgeStorage()


@pytest.fixture
def edge1(measurement):
    return BinaryEdge(
        BasicTestVertex(),
        BasicTestVertex(),
        measurement=measurement,
        noise_model=Isotropic.Sigma(dim=2, sigma=1),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Isotropic.Sigma(dim=2, sigma=1)),
    )


@pytest.fixture
def edge2(measurement):
    return UnaryEdge(
        BasicTestVertex(),
        measurement=measurement,
        noise_model=Isotropic.Sigma(dim=2, sigma=1),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Isotropic.Sigma(dim=2, sigma=1)),
    )


@pytest.fixture
def edge3(measurement):
    return UnaryEdge(
        BasicTestVertex(),
        measurement=measurement,
        noise_model=Isotropic.Sigma(dim=2, sigma=1),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Isotropic.Sigma(dim=2, sigma=1)),
    )


@pytest.fixture
def edge4(measurement):
    return MultiEdge(
        vertices=[BasicTestVertex(), BasicTestVertex(), BasicTestVertex()],
        measurements=[measurement],
        noise_model=Isotropic.Sigma(dim=2, sigma=1),
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=Isotropic.Sigma(dim=2, sigma=1)),
    )


def test_add(edge_storage, edge1, edge2, edge4):

    edge_storage.add(edge1)
    assert edge1 in edge_storage._edges

    edge_storage.add([edge2, edge4])
    assert edge2 in edge_storage._edges
    assert edge4 in edge_storage._edges


def test_add_multiple(edge_storage, edge1, edge2, edge3, edge4):

    edge_storage.add([edge1, edge2, edge3, edge4])
    assert edge1 in edge_storage._edges
    assert edge2 in edge_storage._edges
    assert edge3 in edge_storage._edges
    assert edge4 in edge_storage._edges


def test_remove(edge_storage, edge1, edge2, edge3):

    edge_storage.add(edge1)
    edge_storage.remove(edge1)
    assert edge1 not in edge_storage._edges

    edge_storage.add([edge2, edge3])
    edge_storage.remove([edge2, edge3])
    assert edge2 not in edge_storage._edges
    assert edge3 not in edge_storage._edges


def test_remove_multiple(edge_storage, edge1, edge2, edge3, edge4):

    edge_storage.add([edge1, edge2, edge3, edge4])
    edge_storage.remove([edge1, edge2, edge3, edge4])
    assert edge1 not in edge_storage._edges
    assert edge2 not in edge_storage._edges
    assert edge3 not in edge_storage._edges
    assert edge4 not in edge_storage._edges
    assert len(edge_storage.edges) == 0
