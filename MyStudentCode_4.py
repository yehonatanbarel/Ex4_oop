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

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons)  # , object_hook=lambda d: SimpleNamespace(**d))
## ==================== GET THE POKEMONS FROM THE JSON AND TURN THEM INTO NODE ========================
from Pokemon import Pokemon
from Node import Node

lst_of_pokemon_pokemon = {}
p_id = 1000;
for p in pokemons_obj["Pokemons"]:
    print(p["Pokemon"]["pos"])
    xyz = p["Pokemon"]["pos"].split(",")
    pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
    # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
    lst_of_pokemon_pokemon[p_id] = Pokemon(p_id, p["Pokemon"]["type"], pos)
    p_id = p_id + 1
## *** this will show us like it was in Ex2 *** dict of - (id, NodeData). this wont tell us the type of the edge
lst_of_pokemon_node = {}
p_id = 1000;
for p in pokemons_obj["Pokemons"]:
    # print(p["Pokemon"]["pos"])
    xyz = p["Pokemon"]["pos"].split(",")
    pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
    # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
    lst_of_pokemon_node[p_id] = Node(p_id, pos)
    p_id = p_id + 1
    ## ==================== GET THE POKEMONS FROM THE JSON AND TURN THEM INTO NODE ========================

    ## ==================== FIND OUT THE EDGE OF EACH POKEMON NODE ========================

## =================================== THIS WILL GET THE AGENT ON THE GRAPH ===================================
num_of_agent = client.get_info()
num_of_agent = num_of_agent.partition("agents")[2]
num_of_agent = num_of_agent.replace("\"", '')
num_of_agent = num_of_agent.replace(':', '')
num_of_agent = num_of_agent.replace("}", '')
num_of_agent = int(num_of_agent)
print(f"num_of_agent = {num_of_agent}")
for i in range(num_of_agent):
    client.add_agent('{\"id\":' + str(i) + '}')
## =================================== THIS WILL GET THE AGENT ON THE GRAPH ===================================
## =================================== GET THE AGENT DATA AND PUT THEM IN AGENT CLASS ===================================
from Agent import Agent
from GraphAlgo import GraphAlgo

agents = client.get_agents()
agents_obj = json.loads(agents)
print(f"agent_data = {agents_obj['Agents']}")
# print(f"agent_data = {agents_obj['Agents'][0]['pos']}")
lst_of_agent_agent = {}
p_id = 1000;
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
    lst_of_agent_agent[agent_id] = Agent(agent_id, agent_value, agent_src, agent_dest, agent_speed, agent_pos)
print(f"lst_of_agent_agent = {lst_of_agent_agent}")
print(lst_of_agent_agent)

## *********************************************************************************************************************
graph_json_check = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

from DiGraph import DiGraph
graph_check = json.loads(graph_json_check)#, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
print(f"graph_check = {graph_check}")
graph_algo = GraphAlgo()
graph_algo.load_from_json_2(graph_check)
print(f"graph_algo. = {graph_algo.get_graph()}")
g = DiGraph()

# ==== ADD ALL OF THE NODE TO THE GRAH-ALGO (POK_NODE, AGENT_NODE, NODE IN GIVEN GRAPH)
for pok_node in lst_of_pokemon_node.values():
    graph_algo.get_graph().add_node(pok_node.get_key(),pok_node.get_pos())
for ag_node in lst_of_agent_agent.values():
    graph_algo.get_graph().add_node(ag_node.get_id()+20000,ag_node.get_pos())
print(f"g = {g}")
# graph_algo.load_from_json_2(graph_check)
# graph_algo.__init__(g)
print(f"graph_algo after g = {graph_algo.get_graph()}")

# for vg in lst_of_agent_agent.values():
#     graph_algo.add_node(ag_node.get_id(),ag_node.get_pos())


# print(f"graph_algo.get_graph() = {graph_algo.get_graph()}")
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
            ag.set_dest(int(close_pokemon))
            client.choose_next_edge(
                '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(close_pokemon) + '}')

def upload_graph():
    graph_json_check = client.get_graph()
    graph_check = json.loads(graph_json_check)  # , object_hook=lambda json_dict: SimpleNamespace(**json_dict))
    print(f"graph_check = {graph_check}")
    graph_algo = GraphAlgo()
    graph_algo.load_from_json_2(graph_check)
    print(f"graph_algo. = {graph_algo.get_graph()}")

def find_best_pokemon_for_all2():
    for pok_node in lst_of_pokemon_node.values():
        graph_algo.get_graph().add_node(pok_node.get_key(), pok_node.get_pos())
    for ag_node in lst_of_agent_agent.values():
        graph_algo.get_graph().add_node(ag_node.get_id(), ag_node.get_pos())
    # for ag
## ==================== FIND OUT THE EDGE OF EACH POKEMON NODE ========================


graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

# client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")


# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)
    for agent in agents:
        # if agent.dest == -1:
        find_best_pokemon_for_all()

    client.move()
    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.Nodes)
    #         client.choose_next_edge(
    #             '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
    #         ttl = client.time_to_end()
    #         print(ttl, client.get_info())
    #
    # client.move()

# game over:
