import pytest

from app.mission_graph import GraphEdge, GraphNode, MissionGraph, NodeType


def node(node_id: str, country: str = "tr") -> GraphNode:
    return GraphNode(node_id, NodeType.MISSION, country, "org-1")


def test_graph_accepts_same_country_edge() -> None:
    graph = MissionGraph()
    graph.add_node(node("m1"))
    graph.add_node(node("v1"))
    graph.add_edge(GraphEdge("m1", "v1", "uses_vehicle"))
    assert len(graph.edges()) == 1


def test_graph_rejects_cross_country_edge() -> None:
    graph = MissionGraph()
    graph.add_node(node("m1", "tr"))
    graph.add_node(node("v1", "de"))
    with pytest.raises(PermissionError):
        graph.add_edge(GraphEdge("m1", "v1", "uses_vehicle"))


def test_graph_rejects_unknown_node() -> None:
    graph = MissionGraph()
    graph.add_node(node("m1"))
    with pytest.raises(ValueError):
        graph.add_edge(GraphEdge("m1", "missing", "depends_on"))
