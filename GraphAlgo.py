import json
from os import path

import numpy as np
from matplotlib.patches import ConnectionPatch

from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from DiGraph import DiGraph
from Node import Node
from typing import List, Tuple
import heapq
from collections import deque
import matplotlib.pyplot as plt
import random


class GraphAlgo(GraphAlgoInterface):
    _graph: GraphInterface

    def __init__(self, graph: GraphInterface = None):
        self._graph = graph

        # ## ******** TAKE CARE IS POS IS NONE **********
        if graph is None:
            pass
        elif self.check_if_all_none() == 0:  # if all of them are none so do random 0-10 to all
            self.init_none_random(0, 10, 0, 10)
        elif self.check_if_all_none() == 1:
            pass
        else:
            minX, maxX, minY, maxY = self.minMax()
            self.init_none_random(minX, maxX, minY, maxY)
        # ## ******** TAKE CARE IS POS IS NONE **********


    """
    :return: the directed graph on which the algorithm works on.
    """
    def get_graph(self) -> GraphInterface:
        return self._graph

    """
    Loads a graph from a json file.
    @param file_name: The path to the json file
    @returns True if the loading was successful, False o.w.
    """
    def load_from_json_2(self,json_dict: dict) -> bool:
        try:
            graph: GraphInterface = DiGraph()
            for node in json_dict["Nodes"]:
                if "pos" in node:
                    xyz = node["pos"].split(",")
                    pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
                    graph.add_node(node["id"], pos)
                else:
                    graph.add_node(node["id"])
            for e in json_dict["Edges"]:
                # Notice that it is true that in input json file we get it in different order.
                # we get src,w,dest. but in our given func that we need to do we get as input in this order
                # src,dest,w.
                graph.add_edge(e["src"], e["dest"], e["w"])
            self._graph = graph
            if self.check_if_all_none() == 0:  # if all of them are none so do random 0-10 to all
                self.init_none_random(0, 10, 0, 10)
            elif self.check_if_all_none() == 1:
                pass
            else:
                minX, maxX, minY, maxY = self.minMax()
                self.init_none_random(minX, maxX, minY, maxY)
            return True
        except IOError as e:
            print(e)
        return False

    def load_from_json(self, file_name: str) -> bool:
        if path.exists(file_name):
            graph: GraphInterface = DiGraph()
        try:
            with open(file_name, 'r') as json_file:
                dict = json.load(json_file)
                for node in dict["Nodes"]:
                    if "pos" in node:
                        xyz = node["pos"].split(",")
                        pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
                        graph.add_node(node["id"], pos)
                    else:
                        graph.add_node(node["id"])
                for e in dict["Edges"]:
                    # Notice that it is true that in input json file we get it in different order.
                    # we get src,w,dest. but in our given func that we need to do we get as input in this order
                    # src,dest,w.
                    graph.add_edge(e["src"], e["dest"], e["w"])
                self._graph = graph
            if self.check_if_all_none() == 0:  # if all of them are none so do random 0-10 to all
                self.init_none_random(0, 10, 0, 10)
            elif self.check_if_all_none() == 1:
                pass
            else:
                minX, maxX, minY, maxY = self.minMax()
                self.init_none_random(minX, maxX, minY, maxY)
            return True
        except IOError as e:
            print(e)
        return False

    """
    Saves the graph in JSON format to a file
    @param file_name: The path to the out file
    @return: True if the save was successful, False o.w.
    """

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'w') as f:
                json.dump(self, indent=2, fp=f, default=lambda a: a.__dict__)
                return True
        except IOError as e:
            print(e)
        return False
    """
    Plots the graph.
    If the nodes have a position, the nodes will be placed there.
    Otherwise, they will be placed in a random but elegant manner.
    @return: None
    """

    def plot_graph(self) -> None:
        fig, ax = plt.subplots()
        nodes_keys = self.get_graph().get_all_v().keys()
        for node in nodes_keys:
            node: Node = self.get_graph().get_all_v().get(node)
            x, y,z = node.get_pos()
            curr_point = np.array([x, y])
            xyA = curr_point
            ax.annotate(node.get_key(), (x, y),
                        color='blue',
                        fontsize=13)
            for e in self.get_graph().all_out_edges_of_node(node.get_key()).keys():
                nei_node: Node = self.get_graph().get_all_v().get(e)
                x, y,z = nei_node.get_pos()
                curr_point = np.array([x, y])
                xyB = curr_point
                draw_line = ConnectionPatch(xyA, xyB, "data", "data",
                                            arrowstyle="-|>", connectionstyle='arc3,rad=0.',
                                            mutation_scale=13, fc="black", color="black", shrinkA=6, shrinkB=6)
                ax.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o", color='red', markersize=7, linewidth=10)
                ax.add_artist(draw_line)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Graph Plot")
        plt.show()


    """
    Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
    @param id1: The start node id
    @param id2: The end node id
    @return: The distance of the path, a list of the nodes ids that the path goes through
    """

    def shortest_path(self, id1: int, id2: int) -> float:
        if self.get_graph().get_all_v().get(id1) is None or self.get_graph().get_all_v().get(id2) is None:
            return float('inf'), []
        self.reset_values()
        self.reset_visit()
        return self.dijkstra(id1, id2)

    """
    this dijkstra is for the shortest_path function
    """
    def dijkstra(self, id_1: int, id_2: int) -> (float,List):
        src:Node = self.get_graph().get_all_v().get(id_1)
        dest:Node = self.get_graph().get_all_v().get(id_2)
        heap: heapq = []
        src.set_dist(0)
        src.set_visited(True)
        heapq.heappush(heap, (0, src))
        curr_parent = {}
        final_dij_path = []
        while len(heap) > 0:
            node: Node = heapq.heappop(heap)[1]
            if node.get_key() == dest.get_key():
                break
            if not node.get_visited():
                node.set_visited(True)
            edges = self.get_graph().all_out_edges_of_node(node.get_key())
            for e in edges:
                ni: Node = self.get_graph().get_all_v().get(e)
                if not ni.get_visited():
                    dist = node.get_dist() + edges.get(e)
                    if ni.get_dist() == -1 or dist < ni.get_dist():
                        ni.set_dist(dist)
                        heapq.heappush(heap, (dist, ni))
                        curr_parent[ni.get_key()] = node.get_key()
        if curr_parent.get(id_2) is None:
            return dest.get_dist(),[]
        final_dij_path.insert(0,id_2)
        parent = curr_parent.get(id_2)
        while parent != id_1:
            final_dij_path.insert(0,parent)
            parent = curr_parent.get(parent)
        final_dij_path.insert(0,id_1)
        return dest.get_dist()

    """
    this reset_values and reset_visit for the short_path, dijkstra and dfs functions
    """
    def reset_values(self):
        nodes: dict = self.get_graph().get_all_v()
        for n in nodes:
            nodes.get(n).set_visited(False)
            nodes.get(n).set_dist(float('inf'))

    def reset_visit(self):
        nodes: dict = self.get_graph().get_all_v()
        for n in nodes:
            nodes.get(n).set_visited(False)



    def dfs(self, node_id: int) -> (List[int], float):
        self.reset_visit()
        node_id = int(node_id)
        stack = deque()
        dist = 0
        dfs_path = [node_id]
        stack.append(node_id)  # add the first node to the stack
        node: Node = self.get_graph().get_all_v().get(node_id)
        node.set_visited(True)
        while len(stack) != 0:
            curr = stack.pop()
            for neighbor in self.get_graph().all_out_edges_of_node(curr).keys():
                nei_node: Node = self.get_graph().get_all_v().get(neighbor)
                if not nei_node.get_visited():
                    stack.append(nei_node.get_key())
                    nei_node.set_visited(True)
                    dfs_path.append(nei_node.get_key())
                    dist = dist + self.get_graph().all_out_edges_of_node(curr).get(nei_node.get_key())
        return dfs_path, dist

    """
    Finds the shortest path that visits all the nodes in the list
    :param node_lst: A list of nodes id's
    :return: A list of the nodes id's in the path, and the overall distance
    """
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        return self.dfs(node_lst[0])


    """
    in this function we will find the min / max value of our node pos (x,y) in our graph
    """
    def minMax(self) -> Tuple[float, float, float, float]:
        x = []
        y = []
        for i in self._graph.get_all_v().keys():
            node: Node = self.get_graph().get_all_v().get(i)
            x.append(node.get_x())
            y.append(node.get_y())
        minX = min(x)
        maxX = max(x)
        minY = min(y)
        maxY = max(y)

        return minX, maxX, minY, maxY

    """
    this func will check if all of our node dont have pos.
    if its True - if all of our node wont have pos so we will put random pos between 0-10 (NOTICE: this is in float not int)
    but if its False - that's mean that some node does have pos in them so we will init random pos 
    on the Nodes that have 'None' in their pos between the range we found in the 'minMax' func we did for it
    we have 3 situation: 
    (1) - all of the node have pos
    (-1) - some does and some doesnt
    (0) - all of the node doesnt have pos
    we will take care of this situation when we load our json graph with load func 
    explanation of the output - 
    return 0 - it mean that all of our given node have 'None' as pos 
    return 1 - all of our node have a real pos (not 'None')
    return -1 - some have 'None' and some doesnt 
    """

    def check_if_all_none(self) -> int:
        isNone = 0
        for i in self._graph.get_all_v().keys():
            node: Node = self.get_graph().get_all_v().get(i)
            if node.get_pos() is None:
                isNone += 1
        if isNone == self.get_graph().v_size():
            return 0
        elif isNone == 0:
            return 1
        else:
            return -1

    """
    init the none node pos random float between 0-10
    """

    def init_none_random(self, minX: float, maxX: float, minY: float, maxY: float):
        for i in self._graph.get_all_v().keys():
            node: Node = self.get_graph().get_all_v().get(i)
            if node.get_pos() is None:
                x = random.uniform(minX, maxX)
                y = random.uniform(minY, maxY)
                z = 0
                node.set_pos((x, y, z))

    """
    Finds the node that has the shortest distance to it's farthest node.
    :return: The nodes id, min-maximum distance
    """

    def centerPoint(self) -> (int, float):
        MaxResults = {}
        MinKey = -1
        MinOfAll = float('inf')
        nodes = self._graph.get_all_v()
        for n in nodes:
            max = -1
            for n1 in nodes:
                if (n != n1):
                    dist = self.shortest_path(n, n1)[0]
                    if (dist != float('inf')):
                        if (max < dist):
                            max = dist
            MaxResults[n] = max

        for key, val in MaxResults.items():
            if (MaxResults.get(key) < MinOfAll):
                MinOfAll = MaxResults.get(key)
                MinKey = key

        return MinKey, MinOfAll


if __name__ == '__main__':
    # _graphAlgo = GraphAlgo()
    # _graph = DiGraph()
    # _graph.add_node(0, (2, 3))
    # _graph.add_node(1, (3, 3))
    # _graph.add_node(2, (5, 3))
    # _graph.add_node(3, (5, 3))
    # _graph.add_node(4, (5, 3))
    # _graph.add_node(5, (5, 3))
    # _graph.add_node(6, (5, 3))
    #
    # _graph.add_edge(0, 1, 1)
    # _graph.add_edge(1, 2, 1)
    # _graph.add_edge(2, 3, 1)
    # _graph.add_edge(3, 4, 1)
    # _graph.add_edge(4, 5, 1)
    # _graph.add_edge(5, 6, 1)
    # _graph.add_edge(0, 6, 20)
    # _graphAlgo.__init__(_graph)
    # print(_graphAlgo.shortest_path(0, 4))
    # _graphAlgo.plot_graph()
#
    _graphAlgo = GraphAlgo()
    _graph = DiGraph()
    _graph.add_node(0, (2, 1))
    _graph.add_node(1, (3, 2))
    _graph.add_node(2, (5, 3))
    _graph.add_edge(0, 1, 1)
    _graph.add_edge(1, 2, 1)
    _graph.add_edge(0, 2, 10)
    _graphAlgo.__init__(_graph)
    print(_graphAlgo.shortest_path(0, 2))
    # _graphAlgo.plot_graph()

    # _graphAlgo = GraphAlgo()
    # _graph = DiGraph()
    # _graphAlgo.load_from_json("T0.json")
    # _graphAlgo.plot_graph()

    g = DiGraph()  # creates an empty directed graph
    for n in range(5):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(0, 4, 5)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(1, 3, 1.9)
    g.add_edge(2, 3, 1.1)
    g.add_edge(3, 4, 2.1)
    g.add_edge(4, 2, .5)
    g_algo = GraphAlgo()
    g_algo.__init__(g)

    # print(g_algo.centerPoint())
    print(g_algo.shortest_path(0,2))
    # print(g_algo.TSP([1, 2, 4]))
    # g_algo.plot_graph()
