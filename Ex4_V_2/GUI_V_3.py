import json
import os
from types import SimpleNamespace
import pygame
from pygame import Color, display, gfxdraw
from pygame.constants import RESIZABLE, VIDEORESIZE
import math
from client import Client

from GraphAlgo import GraphAlgo

# init pygame

WIDTH, HEIGHT = 800, 500
pygame.display.set_caption("Pokemon Game!")
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

"""
for the client and get the graph and all
"""
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
client = Client()
client.start_connection(HOST, PORT)
# pokemons = client.get_pokemons()
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

# print(pokemons)

graph_json = client.get_graph()

# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
"""
for the client and get the graph and all
"""

# pokemons = client.get_pokemons()
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
#
# print(pokemons)
#
# graph_json = client.get_graph()


FONT = pygame.font.SysFont('Arial', 20, bold=True)

## =========== put graph for check ========================
# with open('A4.json', 'r') as file:
#     graph = json.load(
#         file, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
## =========== put graph for check ========================

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

print(graph.Edges)
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

## ================== FROM HERE IS THE WORK ON THE SCREEN ====================

def arrow(start, end, d, h, color):
    """
    קרדיט לדביר על הפונקציה
    """

    dx = (end[0] - start[0])
    dy = (end[1] - start[1])
    D = (math.sqrt(dx * dx + dy * dy))
    xm = (D - d)
    xn = (xm)
    ym = (h)
    yn = -h
    sin = dy / D
    cos = dx / D
    x = xm * cos - ym * sin + start[0]
    ym = xm * sin + ym * cos + start[1]
    xm = x
    x = xn * cos - yn * sin + start[0]
    yn = xn * sin + yn * cos + start[1]
    xn = x
    points = [(end[0], end[1]), (int(xm), int(ym)), (int(xn), int(yn))]

    pygame.draw.line(screen, color, start, end, width=4)
    pygame.draw.polygon(screen, color, points)


r = 15
margin = 50
while (True):
    """
    add the pokemon and agent
    """
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    # print(f"=========================================={pokemons}")
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # print(f"=========================================={pokemons}")
    put_agent_on_graph()
    # print(f"************************{client.get_agents()}")
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        # a.src = SimpleNamespace(src=a.src)
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    """
    add the pokemon and agent
    """
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == VIDEORESIZE:
            screen = display.set_mode((event.w, event.h), depth=32, flags=RESIZABLE)

    # refresh screen
    screen.fill(Color(40, 80, 100))

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
        # pygame.draw.line(screen, Color(0, 255, 0),
        #                  (src_x, src_y), (dest_x, dest_y),width=2)
        arrow((src_x, src_y), (dest_x, dest_y), 17, 7, color=(255, 255, 255))

    # for n in graph.Nodes:
    #     x = scale(n.pos.x, margin, screen.get_width() - margin, min_x, max_x)
    #     y = scale(n.pos.y, margin, screen.get_width() - margin, min_y, max_y)
    #     pygame.draw.circle(screen,pygame.Color(221,209,60) , (x,y),r)
    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))
        id_srf = FONT.render(str(n.id), True, pygame.Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)


    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)


    pygame.display.update()
    clock.tick(60)

    print(f"agent dest = {agent.dest}")
    print(f"agent src = {agent.src}")
    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.Nodes)
    #         client.choose_next_edge(
    #             '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
    #         ttl = client.time_to_end()
    #         print(ttl, client.get_info())
    #
    # client.move()
    # client.choose_next_edge(
    #     '{"agent_id":'+str(0)+', "next_node_id":'+str(10)+'}')
    # client.move()
