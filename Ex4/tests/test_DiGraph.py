from unittest import TestCase

from src.DiGraph import DiGraph


class TestDiGraph(TestCase):
    def setUp(self):
        self.g = DiGraph()
        for n in range(4):
            self.g.add_node(n)
        self.g.add_edge(0, 1, 1)
        self.g.add_edge(1, 0, 1.1)
        self.g.add_edge(1, 2, 1.3)
        self.g.add_edge(2, 3, 1.1)
        self.g.add_edge(1, 3, 1.9)
        self.g.remove_edge(1, 3)
        self.g.add_edge(1, 3, 10)

    def test_v_size(self):
        self.assertEqual(4, self.g.v_size())

    def test_e_size(self):
        self.assertEqual(5, self.g.e_size())

    def test_get_all_v(self):
        self.assertEqual(self.g.nodes, self.g.get_all_v())

    def test_all_in_edges_of_node(self):
        self.assertEqual(self.g.edges_in[0], self.g.all_in_edges_of_node(0))
        self.assertEqual(self.g.edges_in[1], self.g.all_in_edges_of_node(1))
        self.assertEqual(self.g.edges_in[2], self.g.all_in_edges_of_node(2))
        self.assertEqual(self.g.edges_in[3], self.g.all_in_edges_of_node(3))

    def test_all_out_edges_of_node(self):
        self.assertEqual(self.g.edges[0], self.g.all_out_edges_of_node(0))
        self.assertEqual(self.g.edges[1], self.g.all_out_edges_of_node(1))
        self.assertEqual(self.g.edges[2], self.g.all_out_edges_of_node(2))
        self.assertEqual(self.g.edges[3], self.g.all_out_edges_of_node(3))

    def test_get_mc(self):
        self.assertEqual(11, self.g.get_mc())

    def test_add_edge(self):
        # self.g.add_edge(1, 0, 1.1)
        self.assertEqual(True, self.g.add_edge(0, 2, 5))
        self.assertEqual(False, self.g.add_edge(0, 2, 5))
        self.assertEqual(False, self.g.add_edge(1, 0, 1.1))
        self.assertEqual(True, self.g.add_edge(1, 0, 2.1))

    def test_add_node(self):
        self.assertEqual(False, self.g.add_node(1))
        self.assertEqual(True, self.g.add_node(4))

    def test_remove_node(self):
        self.assertEqual(True, self.g.remove_node(0))
        self.assertEqual(3, self.g.e_size())

    def test_remove_edge(self):
        self.assertEqual(True, self.g.remove_edge(0, 1))
        self.assertEqual(False, self.g.remove_edge(5, 6))
