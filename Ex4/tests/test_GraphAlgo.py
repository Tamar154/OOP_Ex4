import json
import sys
from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def setUp(self):
        self.g_algo = GraphAlgo()
        self.g_algo.load_from_json("../data/T0.json")

    def test_get_graph(self):
        self.assertEqual(self.g_algo.graph, self.g_algo.get_graph())

    def test_load_from_json(self):
        """
        checking both load_from_json and save_to_json here.
        """
        temp = GraphAlgo()
        self.g_algo.save_to_json("../data/test.json")
        temp.load_from_json("../data/test.json")
        self.assertEqual(str(temp.graph), str(self.g_algo.graph))

    def test_save_to_json(self):
        """
        we already checked save_to_json at the load_from_json test.
        """
        self.assertEqual(True, True)

    def test_shortest_path(self):
        self.assertEqual((2.8, [0, 1, 3]), self.g_algo.shortest_path(0, 3))
        self.assertEqual((1.8, [1, 3]), self.g_algo.shortest_path(1, 3))
        self.assertEqual((sys.float_info.max, None), self.g_algo.shortest_path(3, 2))

    def test_tsp(self):
        self.assertEqual(([0, 1, 2, 3], 3.4), self.g_algo.TSP([0, 1, 2, 3]))

    def test_center_point(self):
        self.g_algo.load_from_json("../data/A0.json")
        self.assertEqual((7, 6.806805834715163), self.g_algo.centerPoint())
        self.g_algo.load_from_json("../data/A1.json")
        self.assertEqual((8, 9.925289024973141), self.g_algo.centerPoint())
        self.g_algo.load_from_json("../data/A2.json")
        self.assertEqual((0, 7.819910602212574), self.g_algo.centerPoint())
        self.g_algo.load_from_json("../data/A3.json")
        self.assertEqual((2, 8.182236568942239), self.g_algo.centerPoint())
        self.g_algo.load_from_json("../data/A4.json")
        self.assertEqual((6, 8.071366078651435), self.g_algo.centerPoint())
        self.g_algo.load_from_json("../data/A5.json")
        self.assertEqual((40, 9.291743173960954), self.g_algo.centerPoint())
