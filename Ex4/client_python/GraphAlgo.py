import json
import random
import sys
import pygame
from typing import List

from pygame.surface import Surface
import matplotlib.pyplot as plt
from client_python.DiGraph import DiGraph
from client_python.Edge import Edge
from client_python.GraphAlgoInterface import GraphAlgoInterface
from client_python.GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g
        self.height = 600
        self.width = 500

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as fp:
                self.graph = DiGraph()
                di = json.load(fp)
                for i in di["Edges"]:
                    e = Edge(**i)
                    # print(e)
                    self.graph.add_edge(e.get_src(), e.get_dest(), e.get_weight())
                for i in di["Nodes"]:
                    if "pos" in i:
                        pos = tuple(map(float, i["pos"].split(',')))
                        self.graph.add_node(i["id"], pos)
                    else:
                        x = random.uniform(35.000, 35.30)
                        y = random.uniform(32.000, 32.30)
                        self.graph.add_node(i["id"], (x, y, 0))
                return True
        except IOError as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as outfile:
                Nodes = []
                Edges = []
                for i in self.graph.edges:
                    for j in self.graph.edges.get(i).values():
                        temp = {"src": j.get_src(), "w": j.get_weight(), "dest": j.get_dest()}
                        Edges.append(temp)
                for i in self.graph.nodes:
                    if "pos" in Nodes:
                        pos_tuple = self.graph.nodes.get(i).get_location()
                        pos = ','.join(tuple(map(str, pos_tuple)))
                        Nodes.append({"pos": pos, "id": self.graph.nodes.get(i).get_key()})
                    else:
                        Nodes.append({"id": self.graph.nodes.get(i).get_key()})
                dictionary = {"Edges": Edges, "Nodes": Nodes}
                outfile.write(json.dumps(dictionary, indent=1))
            return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans = []
        n = self.graph.v_size()
        dis = [[0 for x in range(n)] for y in range(n)]
        nex = [[0 for x in range(n)] for y in range(n)]
        mat = [[0 for x in range(n)] for y in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    mat[i][j] = 0
                else:
                    mat[i][j] = sys.float_info.max
        for i in self.graph.edges:
            for j in self.graph.edges.get(i):
                mat[i][j] = self.graph.edges.get(i).get(j).get_weight()

        for i in range(n):
            for j in range(n):
                dis[i][j] = mat[i][j]
                if mat[i][i] == sys.float_info.max:
                    mat[i][j] = -1
                else:
                    nex[i][j] = j

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dis[i][k] + dis[k][j] < dis[i][j]:
                        dis[i][j] = dis[i][k] + dis[k][j]
                        nex[i][j] = nex[i][k]

        dist = dis[id1][id2]
        if nex[id1][id2] == -1:
            return -1, None

        ans.append(id1)
        while id1 != id2:
            id1 = nex[id1][id2]
            ans.append(id1)

        if dist == sys.float_info.max:
            ans = []
            dist = "inf"
        return dist, ans

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        n = self.graph.v_size()
        temp = []
        for i in range(n):
            temp.append(i)
        mat = [[0 for x in range(n)] for y in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    mat[i][j] = 0
                else:
                    mat[i][j] = sys.float_info.max
        for i in self.graph.edges:
            for j in self.graph.edges.get(i):
                mat[i][j] = self.graph.edges.get(i).get(j).get_weight()
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if mat[i][k] + mat[k][j] < mat[i][j]:
                        mat[i][j] = mat[i][k] + mat[k][j]

        counter = 0
        j = 0
        i = 0
        list_size = len(temp)
        minimum = sys.float_info.max
        visited = [temp[0]]
        route = [0 for x in range(n)]
        while i < list_size and j < list_size:
            if counter >= list_size - 1:
                break
            # if node_lst[j] < len(visited):
            # if j != i and visited.__contains__(node_lst[j]) is False:
            if j != i and not (temp[j] in visited):
                if mat[i][j] < minimum:
                    minimum = mat[i][j]
                    route[counter] = j + 1
            j += 1
            if j == list_size:
                minimum = sys.float_info.max
                visited.append(temp[route[counter] - 1])
                j = 0
                i = route[counter] - 1
                counter += 1

        ans = []
        size = len(node_lst)
        start = visited.index(node_lst[0])
        end = visited.index(node_lst[size - 1])
        i = 0
        while i < len(visited):
            if start <= i <= end:
                ans.append(visited[i])
            i += 1
        weight = 0

        i = 0
        while i < len(ans) - 1:
            weight += self.graph.edges.get(ans[i]).get(ans[i + 1]).get_weight()
            i += 1
        return ans, weight

    def centerPoint(self) -> (int, float):
        n = self.graph.v_size()
        D = [[0 for x in range(n)] for y in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    D[i][j] = 0
                else:
                    D[i][j] = sys.float_info.max
        for i in self.graph.edges:
            for j in self.graph.edges.get(i):
                D[i][j] = self.graph.edges.get(i).get(j).get_weight()
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if D[i][k] + D[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + D[k][j]

        temp = [0 for x in range(n)]
        for i in range(n):
            temp[i] = 0
            for j in range(n):
                if temp[i] < D[i][j]:
                    temp[i] = D[i][j]

        maximum = 99999.0
        for i in range(n):
            if maximum > temp[i]:
                maximum = temp[i]
        ans = 0
        for i in range(n):
            if temp[i] == sys.float_info.max:
                return None, "inf"

        for i in range(n):
            if temp[i] == maximum:
                for j in range(len(D[i])):
                    if D[i][j] > ans:
                        ans = D[i][j]
                return i, ans
        return None, "inf"

    def plot_graph(self) -> None:
        x = []
        y = []
        for i in self.graph.nodes:
            node = self.graph.nodes.get(i)
            x.append(node.get_x())
            y.append(node.get_y())
        i = 0

        for i in self.graph.edges.values():
            for j in i.values():
                edge = j
                plt.arrow(x[edge.get_src()], y[edge.get_src()], x[edge.get_dest()] - x[edge.get_src()],
                          y[edge.get_dest()] - y[edge.get_src()], width=0.00005, head_width=0.0003,
                          head_length=0.0003,
                          length_includes_head=True, color="black")

        plt.scatter(x, y, color='r')
        i = 0
        while i < len(x):
            plt.text(x[i], y[i], i, fontdict=None, fontsize=15, color='b')
            i += 1
        plt.show()

    def scale_x(self, x):
        return self.width * (x - self.min_x()) // (self.max_x() - self.min_x())

    def scale_y(self, y):
        return self.height * (self.max_y() - y) // (self.max_y() - self.min_y())

    def max_x(self) -> int:
        maximum = sys.float_info.min
        temp = 0
        for i in self.graph.nodes:
            temp = self.graph.nodes.get(i).get_x()
            if temp > maximum:
                maximum = temp
        return maximum

    def min_x(self) -> int:
        minimum = sys.float_info.max
        temp = 0
        for i in self.graph.nodes:
            temp = self.graph.nodes.get(i).get_x()
            if temp < minimum:
                minimum = temp
        return minimum

    def max_y(self) -> int:
        maximum = sys.float_info.min
        temp = 0
        for i in self.graph.nodes:
            temp = self.graph.nodes.get(i).get_y()
            if temp > maximum:
                maximum = temp
        return maximum

    def min_y(self) -> int:
        minimum = sys.float_info.max
        temp = 0
        for i in self.graph.nodes:
            temp = self.graph.nodes.get(i).get_y()
            if temp < minimum:
                minimum = temp
        return minimum

