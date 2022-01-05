from GraphInterface import GraphInterface
from Node import Node


class DiGraph(GraphInterface):

    _nodes: dict
    _edgesOut: dict
    _edgesInside: dict
    _mc: int
    _numOfEdges: int
    _numOfNodes: int


    def __init__(self):
        self._nodes: dict = {}
        self._edgesOut: dict = {}  # dict of dict
        self._edgesInside: dict = {}  # dict of dict
        self._numOfEdges: int = 0
        self._numOfNodes: int = 0
        self._mc: int = 0

    def v_size(self) -> int:  # 'v' is for vertex - node
        return self._numOfNodes

    def e_size(self) -> int:
        return self._numOfEdges

    def get_mc(self) -> int:
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self._nodes or id2 not in self._nodes or id1 == id2:
            return False
        elif  id2 in self._edgesOut[id1]:
            return False
        else:
            self._edgesOut[id1].update({id2: weight})
            self._edgesInside[id2].update({id1: weight})
            self._numOfEdges += 1
            self._mc += 1
            return True

    # every time we add a node we will also add  it to our edges (in\out)
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes:
            return False
        self._nodes[node_id] = Node(node_id, pos)
        self._edgesOut[node_id] = {}  # because he doesnt have a neighbor yet
        self._edgesInside[node_id] = {}  # because he doesnt have a neighbor yet
        self._numOfNodes+=1
        self._mc += 1

        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes:
            return False
        # from numOfEdge we need to del all of the edge we del when we del node id1
        numOfEdgeOutFromNode_id = len(self.all_out_edges_of_node(node_id))
        numOfEdgeInsideFromNode_id = len(self.all_in_edges_of_node(node_id))
        del self._nodes[node_id]
        del self._edgesOut[node_id]  # this will delete all of the edges that comes out from the deleted node
        del self._edgesInside[node_id]  # this will delete all of the edges that comes in from the deleted node
        self._mc += 1
        self._numOfNodes -= 1
        self._numOfEdges -= (numOfEdgeOutFromNode_id + numOfEdgeInsideFromNode_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._nodes or node_id2 not in self._nodes:
            return False
        if node_id2 not in self.all_out_edges_of_node(node_id1):
            return False
        del (self._edgesOut[node_id1][node_id2])
        del (self._edgesInside[node_id2][node_id1])
        self._numOfEdges -= 1
        self._mc += 1
        return True


    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        if id1 not in self._nodes.keys():
            return {}
        # if it doesit will return the inner dict for the KEY:'id1' in '_edgesInside' outer dict
        return self._edgesInside.get(id1)  # return all of the nodes neighbors (dict of dict)

    def all_out_edges_of_node(self, id1: int) -> dict:
        if id1 not in self._nodes.keys():
            return {}
        # if it doesnt will return the inner dict for the KEY:'id1' in '_edgesOut' outer dict
        return self._edgesOut.get(id1)  # return all of the nodes neighbors (dict of dict)

    def __repr__(self):
        return self._nodes.__repr__()