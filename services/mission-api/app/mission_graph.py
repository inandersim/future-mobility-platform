from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class NodeType(StrEnum):
    MISSION = "mission"
    VEHICLE = "vehicle"
    OPERATOR = "operator"
    ROUTE = "route"
    CORRIDOR = "corridor"
    AIRSPACE = "airspace"
    WEATHER = "weather"
    ENERGY = "energy"
    RISK = "risk"
    EMERGENCY = "emergency"
    REGULATION = "regulation"
    INFRASTRUCTURE = "infrastructure"


@dataclass(frozen=True)
class GraphNode:
    id: str
    node_type: NodeType
    country_id: str
    organization_id: str


@dataclass(frozen=True)
class GraphEdge:
    source_id: str
    target_id: str
    relation: str


class MissionGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: set[GraphEdge] = set()

    def add_node(self, node: GraphNode) -> None:
        if node.id in self._nodes:
            raise ValueError(f"duplicate graph node: {node.id}")
        self._nodes[node.id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        source = self._nodes.get(edge.source_id)
        target = self._nodes.get(edge.target_id)
        if source is None or target is None:
            raise ValueError("graph edge references an unknown node")
        if source.country_id != target.country_id:
            raise PermissionError("cross-country mission graph edge denied")
        self._edges.add(edge)

    def nodes(self) -> tuple[GraphNode, ...]:
        return tuple(self._nodes.values())

    def edges(self) -> tuple[GraphEdge, ...]:
        return tuple(self._edges)
