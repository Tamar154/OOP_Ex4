import collections

from Edge import Edge
from GraphInterface import GraphInterface
from collections import defaultdict
from Node import Node


class DiGraph(GraphInterface):
    def __init__(self):
        self.nodes = {}  # {node_id : Node}
        self.edges = defaultdict(dict)
        self.edges_in = defaultdict(dict)
        self.mc = 0

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        counter = 0
        for i in self.edges:
            counter += len(self.edges.get(i))
        return counter

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.edges_in[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edges[id1]

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.edges and id2 not in self.edges[id1]:
            self.mc += 1
        elif id1 in self.edges and id2 not in self.edges[id1]:
            self.mc += 1
        elif self.edges.get(id1).get(id2).get_weight() != weight:
            self.mc += 1
        else:
            return False
        e = Edge(id1, weight, id2)
        self.edges[id1][id2] = e
        self.edges_in[id2][id1] = e
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        n = Node(pos, node_id)
        if node_id not in self.nodes:
            self.nodes[node_id] = n
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        if self.nodes.get(node_id) is not None:
            self.mc += 1
            self.edges.pop(node_id)
            for i in self.edges:
                if self.edges.get(i).get(node_id) is not None:
                    self.edges.get(i).pop(node_id)
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self.edges and node_id2 in self.edges[node_id1]:
            self.mc += 1
        elif node_id1 not in self.edges and node_id2 in self.edges[node_id1]:
            self.mc += 1
        else:
            return False
        self.edges.get(node_id1).pop(node_id2)
        self.edges_in.get(node_id2).pop(node_id1)
        return True

    def __str__(self) -> str:
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"

    def __repr__(self) -> str:
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"
