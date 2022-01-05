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
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d)) --- IN THE EXAMPLE HE DID IT BUT I CHEANGE
pokemons_obj = json.loads(pokemons)

print(f"========= pokemons ================={pokemons}")
print(f"========= pokemons_obj ================={pokemons_obj}")
z = pokemons_obj["Pokemons"]  # [0]["Pokemon"]["pos"]
print(f"zzzzzzzzzzzz{z}")

## =================== IN HERE I GET THE LIST OF ALL POKEMON I GAVE THEM AN ID AND THEY HOLD TYP AND POS ============
lst_of_pokemon_node = {}
p_id = 1000;
for p in pokemons_obj["Pokemons"]:
    # print(p["Pokemon"]["pos"])
    xyz = p["Pokemon"]["pos"].split(",")
    pos = float(xyz[0]), float(xyz[1]), float(xyz[2])
    print(pos)
    # lst_of_pokemon_node[p["Pokemon"]["type"]] = pos
    lst_of_pokemon_node[p_id] = p["Pokemon"]["type"], pos
    p_id = p_id + 1

    # lst_of_pokemon_node.append(p["Pokemon"]["type"],pos)
print(f"lst_of_pokemon_node - {lst_of_pokemon_node}")
## =================== IN HERE I GET THE LIST OF ALL POKEMON I GAVE THEM AN ID AND THEY HOLD TYP AND POS ============

## ================== FIND OUT THE EGDE OF THE POKEMON ======================
import math

graph_json_check = client.get_graph()
graph_check = json.loads(graph_json_check)  # , object_hook=lambda json_dict: SimpleNamespace(**json_dict))
print(graph_check['Edges'])
print(graph_check['Nodes'][0]['pos'])
x = graph_check['Nodes'][0]['pos'].split(',')[0]
y = graph_check['Nodes'][0]['pos'].split(',')[1]
x = float(x)
y = float(y)
print(x)
print(y)
b = list(list(lst_of_pokemon_node.values()))
print(b[0])
print(graph_check['Edges'])
print(graph_check['Nodes'])
# print(math.dist((x,,y))
print("===========================================================================================================")
# print(list(list(lst_of_pokemon_node.values())[0])[1])
# print(list(lst_of_pokemon_node.keys())[0])
# print(lst_of_pokemon_node)
dist_of_pok_id_and_his_edge_as_node = {}
# itereate on the values of our pokemon key is the id and the value is (type,(pos) )
# for p in lst_of_pokemon_node.values():
from Node import Node

for k in range(len(lst_of_pokemon_node.values())):
    pokemon_to_check_dist = list(
        list(lst_of_pokemon_node.values())[k])  # this is: b = list(list(lst_of_pokemon_node.values())) - b[0]
    for i in range(len(graph_check['Nodes'])):
        x_1 = float(graph_check['Nodes'][i]['pos'].split(',')[0])
        y_1 = float(graph_check['Nodes'][i]['pos'].split(',')[1])
        for j in range(len(graph_check['Nodes'])):
            x_2 = float(graph_check['Nodes'][j]['pos'].split(',')[0])
            y_2 = float(graph_check['Nodes'][j]['pos'].split(',')[1])
            dist_xy = math.dist((x_1, y_1), (x_2, y_2))
            # pokemon_to_check_dist[0] = b[0][0], pokemon_to_check_dist[1] = b[0][1]
            pok_x = pokemon_to_check_dist[1][0]
            pok_y = pokemon_to_check_dist[1][1]
            dist_pokemon_src_dest = math.dist((float(pok_x), float(pok_y)), (x_1, y_1)) + math.dist(
                (float(pok_x), float(pok_y)), (x_2, y_2))
            # if he is on this edge
            if dist_xy - dist_pokemon_src_dest < 0.1 or dist_xy == dist_pokemon_src_dest - 0.1:  # 97656770719604:
                # we will now check the type of this pokemon (up \ down)
                if float(list(lst_of_pokemon_node.keys())[k]) < 0:  # it goes down
                    low = min(graph_check['Nodes'][i]['id'], graph_check['Nodes'][j]['id'])  # low is the - src, up is the - dest
                    up = max(graph_check['Nodes'][i]['id'], graph_check['Nodes'][j]['id'])
                else:  # if it goes up so
                    low = max(graph_check['Nodes'][i]['id'], graph_check['Nodes'][j]['id'])  # low is the - src, up is the - dest
                    up = min(graph_check['Nodes'][i]['id'], graph_check['Nodes'][j]['id'])
                pok_node = Node(list(lst_of_pokemon_node.keys())[k], (pokemon_to_check_dist[0], pokemon_to_check_dist[1]))
                dist_of_pok_id_and_his_edge_as_node[pok_node.get_key()] = pok_node, (low, up)

print(dist_of_pok_id_and_his_edge_as_node)

## ================== FIND OUT THE EGDE OF THE POKEMON ======================

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

client.add_agent("{\"id\":0}")
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
    # print(f"=========================================={pokemons}")
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

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over:
