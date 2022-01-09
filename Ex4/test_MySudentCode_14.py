import networkx as nx
import math
from unittest import TestCase
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface


EPS = 0.001

graph_x_test = nx.DiGraph()
graph_x_test.add_node(0, pos=(35.18753053591606, 32.10378225882353), value=0, type=0)
graph_x_test.add_node(1, pos=(35.18958953510896, 32.10785303529412), value=0, type=0)
graph_x_test.add_node(10, pos=(35.18910131880549, 32.103618700840336), value=0, type=0)
graph_x_test.add_node(2, pos=(35.19341035835351, 32.10610841680672), value=0, type=0)
graph_x_test.add_node(3, pos=(35.197528356739305, 32.1053088), value=0, type=0)
graph_x_test.add_node(4, pos=(35.2016888087167, 32.10601755126051), value=0, type=0)
graph_x_test.add_node(5, pos=(35.20582803389831, 32.10625380168067), value=0, type=0)
graph_x_test.add_node(6, pos=(35.20792948668281, 32.10470908739496), value=0, type=0)
graph_x_test.add_node(7, pos=(35.20746249717514, 32.10254648739496), value=0, type=0)
graph_x_test.add_node(8, pos=(35.20319591121872, 32.1031462), value=0, type=0)
graph_x_test.add_node(9, pos=(35.19597880064568, 32.10154696638656), value=0, type=0)
graph_x_test.add_node(999, pos=(35.189, 32.107), value=0, type=1)
graph_x_test.add_node(-999, pos=(35.189, 32.107), value=0, type=-1)

graph_x_test.add_edge(0, 1)
graph_x_test.add_edge(1, 0)
graph_x_test.add_edge(1, 2)
graph_x_test.add_edge(2, 1)
graph_x_test.add_edge(2, 3)
graph_x_test.add_edge(3, 2)
graph_x_test.add_edge(3, 4)
graph_x_test.add_edge(4, 3)
graph_x_test.add_edge(4, 5)
graph_x_test.add_edge(5, 4)
graph_x_test.add_edge(5, 6)
graph_x_test.add_edge(6, 5)
graph_x_test.add_edge(6, 7)
graph_x_test.add_edge(7, 6)
graph_x_test.add_edge(7, 8)
graph_x_test.add_edge(8, 7)
graph_x_test.add_edge(8, 9)
graph_x_test.add_edge(9, 10)
graph_x_test.add_edge(10,0)
graph_x_test.add_edge(0,10)

def find_pokemon_edge_test_2(pokemon_id):
    pokemon_id_src_x = graph_x_test.nodes.get(pokemon_id)['pos'][0]  # x
    pokemon_id_src_y = graph_x_test.nodes.get(pokemon_id)['pos'][1]  # y

    for edge in list(graph_x_test.edges):
        edge_src = edge[0]  # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x_test.nodes.get(edge_src)['pos'][0]  # x
        edge_src_y = graph_x_test.nodes.get(edge_src)['pos'][1]  # y
        edge_dest_x = graph_x_test.nodes.get(edge_dest)['pos'][0]  # x
        edge_dest_y = graph_x_test.nodes.get(edge_dest)['pos'][1]  # y
        dist_src_edge = math.sqrt((edge_src_x - edge_dest_x) ** 2 + ((edge_src_y - edge_dest_y) ** 2))
        dist_src_n = math.sqrt((edge_src_x - pokemon_id_src_x) ** 2 + ((edge_src_y - pokemon_id_src_y) ** 2))
        dist_n_dest = math.sqrt((pokemon_id_src_x - edge_dest_x) ** 2 + ((pokemon_id_src_y - edge_dest_y) ** 2))
        if abs(dist_src_edge - (dist_src_n + dist_n_dest)) < EPS:
            if graph_x_test.nodes[pokemon_id]['type'] > 0:  # if type == 1
                return min(edge_src, edge_dest) , max(edge_src, edge_dest)
            else:
                return max(edge_src, edge_dest) , min(edge_src, edge_dest)


class Test(TestCase):
    def test_find_pokemon_edge_test_2(self):
        self.assertEqual(find_pokemon_edge_test_2(999), (0,1))
        self.assertEqual(find_pokemon_edge_test_2(-999), (1,0))

class TestGraphAlgo(TestCase):
    def setUp(self):
        self.ga0: GraphAlgoInterface = GraphAlgo()
        self.ga1: GraphAlgoInterface = GraphAlgo()
        self.ga2: GraphAlgoInterface = GraphAlgo()
        self.ga3: GraphAlgoInterface = GraphAlgo()
        self.ga4: GraphAlgoInterface = GraphAlgo()
        self.ga5: GraphAlgoInterface = GraphAlgo()
        self.ga0.load_from_json('A0.json')
        self.ga1.load_from_json('A1.json')
        self.ga2.load_from_json('A2.json')
        self.ga3.load_from_json('A3.json')
        self.ga4.load_from_json('A4.json')
        self.ga5.load_from_json('A5.json')

    def test_get_load_save_graph(self):
        _graphAlgo = GraphAlgo()
        _graph = DiGraph()
        _graph.add_node(0, (2, 3))
        _graph.add_node(1, (3, 3))
        _graph.add_node(2, (5, 3))
        _graph.add_node(3, (2, 5))
        _graph.add_edge(0, 1, 1)
        _graph.add_edge(1, 2, 1)
        _graph.add_edge(2, 3, 1)

        _graphAlgo.__init__(_graph)
        GraphToGet = _graphAlgo.get_graph()
        self.assertEqual(4, GraphToGet.v_size())
        self.assertEqual(3, GraphToGet.e_size())

        self.GraphToLoad: GraphAlgoInterface = GraphAlgo()
        self.GraphToLoad.load_from_json('A0.json')
        self.assertEqual(32, self.GraphToLoad.__sizeof__())

    def test_plot_graph(self):
        _graphAlgo = GraphAlgo()
        _graph = DiGraph()
        _graph.add_node(0, (2, 3))
        _graph.add_node(1, (3, 3))
        _graph.add_node(2, (8, 5))
        _graph.add_node(3, (5, 2))
        _graph.add_node(4, (6, 4))
        _graph.add_edge(0, 1, 2)
        _graph.add_edge(0, 2, 4)
        _graph.add_edge(2, 4, 5)
        _graph.add_edge(1, 3, 3)
        _graph.add_edge(3, 0, 4)
        _graph.add_edge(3, 1, 6)
        _graph.add_edge(4, 2, 2)
        _graphAlgo.__init__(_graph)
        dic = _graphAlgo.get_graph().get_all_v()
        for x in dic:
            n1 = _graphAlgo.get_graph().get_all_v().get(x).get_pos()

    def test_tsp(self):
        _graphAlgo = GraphAlgo()
        _graph = DiGraph()
        _graph.add_node(0, (2, 3))
        _graph.add_node(1, (3, 3))
        _graph.add_node(2, (5, 3))
        _graph.add_node(3, (5, 2))
        _graph.add_node(4, (2, 9))
        _graph.add_edge(0, 1, 1)
        _graph.add_edge(1, 2, 1)
        _graph.add_edge(3, 2, 10)

        _graphAlgo.__init__(_graph)
        self.assertEqual(([0, 1, 2], 2), (_graphAlgo.TSP([0])))


