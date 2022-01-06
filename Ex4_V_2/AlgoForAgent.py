"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
import math
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
from pygame import *


# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)


FONT = pygame.font.SysFont('Arial', 20, bold=True)

## ============================= IMPORT =============================
from client import Client
from Pokemon import Pokemon
from Node import Node
from Agent import Agent
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph
import json
## =============================  IMPORT  =============================
## ============================= LIST  =============================
lst_of_pokemon_pokemon = {}
lst_of_pokemon_node = {}
lst_of_agent_agent = {}

## =============================  LIST  =============================
## =============================  ALL JSON LOAD - GRAPH,POKEMON, AGENT (GET_INFO GAVE ME ERROR SO I LEFT IT INSIDE FUNCTION 'PUT_AGENT_ON_GRAPH')  =============================

graph_json_check = client.get_graph()
graph = json.loads(graph_json_check)  # , object_hook=lambda json_dict: SimpleNamespace(**json_dict))
graph_algo = GraphAlgo()
graph_algo.load_from_json_2(graph)


pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons)  # , object_hook=lambda d: SimpleNamespace(**d))



## =============================  ALL JSON LOAD  =============================

## ==================== GET THE POKEMONS FROM THE JSON AND TURN THEM INTO NODE ========================

"""
the format is like this -  Pokemon(value,type , pos, id)
{{1000: <Pokemon.Pokemon object at 0x0000024A36F4E580>}
if we remove the comment from __reper__ in pokemon it will look like this
{1000: 1000: vlaue: 5.0, type: -1, pos: (35.197656770719604, 32.10191878639921, 0.0), id: 1000}

**** NOTICE THAT THE POKEMON DIDNT CAME WITH AN ID FROM THE JSON, I GAVE THEM THE ID BECAUSE IN THE SHORTPATH ALGO IS BASED ON THE NODE ID
**** THE ID OF THE POKEMON WILL START FROM '1000'
"""
def make_lst_of_pokemon_pokemon():
    p_id = 1000;
    for p in pokemons_obj["Pokemons"]:
        print(p["Pokemon"]["pos"])
        value = p["Pokemon"]["value"]
        type = p["Pokemon"]["type"]
        id = p_id
        xyz = p["Pokemon"]["pos"].split(",")
        pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
        # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
        lst_of_pokemon_pokemon[p_id] = Pokemon(value,type , pos, id)
        p_id = p_id + 1
## *** this will show us like it was in Ex2 *** dict of - (id, NodeData). this wont tell us the type of the edge
"""
the format is like this - Node(p_id,  pos) - without the type p["Pokemon"]["type"]
with the node __reper__
{1000: id: 1000, pos: (35.197656770719604, 32.10191878639921, 0.0)}
"""
def make_lst_of_pokemon_node():
    p_id = 1000;
    for p in pokemons_obj["Pokemons"]:
        # print(p["Pokemon"]["pos"])
        xyz = p["Pokemon"]["pos"].split(",")
        pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
        # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
        lst_of_pokemon_node[p_id] = Node(p_id, pos)
        p_id = p_id + 1
    ## ==================== GET THE POKEMONS FROM THE JSON AND TURN THEM INTO NODE ========================


## =================================== THIS WILL GET THE AGENT ON THE GRAPH && GET THE AGENT DATA AND PUT THEM IN AGENT CLASS ===================================

"""
========================= IMPORTANT TO NOTE THAT IN ORDER TO USE THE FUNCTION make_lst_of_agent_agent WE NEED TO USE THE FUCNTION =========================
========================= put_agent_on_graph SO THEY WILL FIRST BE ON THE GRAPH =========================
"""
def put_agent_on_graph():
    num_of_agent = client.get_info()
    num_of_agent = num_of_agent.partition("agents")[2]
    num_of_agent = num_of_agent.replace("\"", '')
    num_of_agent = num_of_agent.replace(':', '')
    num_of_agent = num_of_agent.replace("}", '')
    num_of_agent = int(num_of_agent)
    print(f"num_of_agent = {num_of_agent}")
    for i in range(num_of_agent):
        client.add_agent('{\"id\":' + str(i) + '}')
"""
## get_the_agent_from_json_and_put_them_in_agent_class in this format - Agent(agent_id, agent_value, agent_src, agent_dest, agent_speed, agent_pos)
{0: <Agent.Agent object at 0x000001927B4B1550>}
with __reper__ in agent
{0: id: 0, value: 0.0, src: 0, dest: -1, speed: 1.0, pos: (35.18753053591606, 32.10378225882353, 0.0)}

**** NOTICE THAT THE AGENT CAME WITH AN ID FROM THE JSON, BUT I CHANGE THE ID TO START FROM '2000' BECAUSE IT WILL HAVE THE SAME ID AS SOME NODE'S,
**** SO IN ORDER TO REMOVE DUPLICATE I CHANGE THE FIRST ID OF THE AGENT TO START FROM '2000'
**** THE ID OF THE POKEMON WILL START FROM '2000'
"""

def make_lst_of_agent_agent():
    agents = client.get_agents()
    agents_obj = json.loads(agents)
    print(f"agent_data = {agents_obj['Agents']}")
    # print(f"agent_data = {agents_obj['Agents'][0]['pos']}")
    for ag in agents_obj['Agents']:
        # print(ag["Agent"]["pos"])
        # print(p["Pokemon"]["pos"])
        agent_id = ag["Agent"]["id"]
        agent_value = ag["Agent"]["value"]
        agent_src = ag["Agent"]["src"]
        agent_dest = ag["Agent"]["dest"]
        agent_speed = ag["Agent"]["speed"]
        xyz = ag["Agent"]["pos"].split(",")
        agent_pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
        # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
        lst_of_agent_agent[agent_id] = Agent(agent_id + 2000, agent_value, agent_src, agent_dest, agent_speed, agent_pos)
    print(f"lst_of_agent_agent = {lst_of_agent_agent}")
    print(lst_of_agent_agent)

## =================================== THIS WILL GET THE AGENT ON THE GRAPH && GET THE AGENT DATA AND PUT THEM IN AGENT CLASS ===================================

def put_all_in_graph_algo_so_we_can_use_short_path_and_load_from_json_2():
    # load the json string into SimpleNamespace Object
    # ==== ADD ALL OF THE NODE TO THE GRAH-ALGO (POK_NODE, AGENT_NODE, NODE IN GIVEN GRAPH)
    for pok_node in lst_of_pokemon_node.values():
        graph_algo.get_graph().add_node(pok_node.get_key(),pok_node.get_pos())
    for ag_node in lst_of_agent_agent.values():
        graph_algo.get_graph().add_node(ag_node.get_id(),ag_node.get_pos())

## =================================== GET THE AGENT DATA AND PUT THEM IN AGENT CLASS ===================================
def find_best_pokemon_for_all():
    for ag in lst_of_agent_agent.values():
        if ag.get_dest() == -1:  # if this agent dont have where to go
            print(f"lst_of_agent_agent.values() = {lst_of_agent_agent.values()}")
            agent_id = ag.get_id()
            print(agent_id)
            agent_pos = float(ag.get_pos()[0]), float(ag.get_pos()[1]), float(ag.get_pos()[2])
            agent_node = Node(agent_id, agent_pos)
            lst_of_pokemon_id_to_go = []
            for p in lst_of_pokemon_node.values():
                dist = GraphAlgo.shortest_path(graph_algo,agent_id, p.get_key())
                lst_of_pokemon_id_to_go.append(dist)
            close_pokemon = min(lst_of_pokemon_id_to_go)
            print(f"====================={close_pokemon}")
            print(f"====================={lst_of_pokemon_id_to_go}")
            print(f"close_pokemon = {close_pokemon}")
            print(f"close_pokemon = {graph['Nodes']}")
            ag.set_dest(int(close_pokemon))
            client.choose_next_edge(
                '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(close_pokemon) + '}')

# client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")


# this commnad starts the server - the game is running now
print(client.is_running())
client.start()
make_lst_of_pokemon_pokemon()
make_lst_of_pokemon_node()
put_agent_on_graph()
make_lst_of_agent_agent()
put_all_in_graph_algo_so_we_can_use_short_path_and_load_from_json_2()
print(client.is_running())


"""
***********************************  GUI ***********************************
"""
def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


min_x=min_y=max_x=max_y=0
def min_max():
    global min_x,min_y,max_x,max_y
    x_lst = []
    y_lst = []
    for i in graph_algo.get_graph().get_all_v().keys():
        node: Node = graph_algo.get_graph().get_all_v().get(i)
        x_lst.append(node.get_x())
        y_lst.append(node.get_y())
    min_x = min(x_lst)
    min_y = min(y_lst)
    max_x = max(x_lst)
    max_y = max(y_lst)


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)

radius = 15




# while client.is_running() == 'true':





if __name__ == '__main__':
    print(client.is_running())
    client.start()
    pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
    make_lst_of_pokemon_pokemon()
    make_lst_of_pokemon_node()
    put_agent_on_graph()
    make_lst_of_agent_agent()
    put_all_in_graph_algo_so_we_can_use_short_path_and_load_from_json_2()
    print(client.is_running())












"""
def plot_graph() -> None:
    fig, ax = plt.subplots()
    nodes_keys = graph_algo.get_graph().get_all_v().keys()
    for node in nodes_keys:
        node: Node = graph_algo.get_graph().get_all_v().get(node)
        x, y,z = node.get_pos()
        curr_point = np.array([x, y])
        xyA = curr_point
        ax.annotate(node.get_key(), (x, y),
                    color='blue',
                    fontsize=13)
        for e in graph_algo.get_graph().all_out_edges_of_node(node.get_key()).keys():
            nei_node: Node = graph_algo.get_graph().get_all_v().get(e)
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


# if __name__ == '__main__':
#     put_agent_on_graph()
#     make_lst_of_agent_agent()
#     print(f"============{list(graph_algo.get_graph().get_all_v().values())}")
#     # plot_graph()


# game over:
