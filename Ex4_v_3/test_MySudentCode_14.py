from unittest import TestCase
import networkx as nx
from MySudentCode_14 import find_pokemon_edge_test


class Test(TestCase):
    def test_find_pokemon_edge_test(self):
        grah_x_test = nx.DiGraph()
        grah_x_test.add_node(0, pos=(35.18753053591606, 32.10378225882353), value=0, type=0)
        grah_x_test.add_node(1, pos=(35.18958953510896, 32.10785303529412), value=0, type=0)
        grah_x_test.add_node(10, pos=(35.18910131880549, 32.103618700840336), value=0, type=0)
        grah_x_test.add_node(2, pos=(35.19341035835351, 32.10610841680672), value=0, type=0)
        grah_x_test.add_node(3, pos=(35.197528356739305, 32.1053088), value=0, type=0)
        grah_x_test.add_node(4, pos=(35.2016888087167, 32.10601755126051), value=0, type=0)
        grah_x_test.add_node(5, pos=(35.20582803389831, 32.10625380168067), value=0, type=0)
        grah_x_test.add_node(6, pos=(35.20792948668281, 32.10470908739496), value=0, type=0)
        grah_x_test.add_node(7, pos=(35.20746249717514, 32.10254648739496), value=0, type=0)
        grah_x_test.add_node(8, pos=(35.20319591121872, 32.1031462), value=0, type=0)
        grah_x_test.add_node(9, pos=(35.19597880064568, 32.10154696638656), value=0, type=0)
        grah_x_test.add_node(999, pos=(35.189, 32.107), value=0, type=0)
        print(grah_x_test.nodes.data())
        print(find_pokemon_edge_test(999))
