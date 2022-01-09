"""
@authors - Yehonatan Barel
           Nadav Moyal
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from GraphAlgo import GraphAlgo
import networkx as nx
from Node import Node
import math

# init pygame
WIDTH, HEIGHT = 1080, 720
call = {}
flag = 0
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption("Pokemon Game!")
icon = pygame.image.load("Pokemon_icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

EPS = 0.00001

"""
find the edge a pokemon is on based on it's pokemon id
"""
def find_pokemon_edge_test(pokemon_id):
    pokemon_id_src_x = graph_x.nodes.get(pokemon_id)['pos'][0]  # x
    pokemon_id_src_y = graph_x.nodes.get(pokemon_id)['pos'][1]  # y

    for edge in list(graph_x.edges):
        edge_src = edge[0]  # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x.nodes.get(edge_src)['pos'][0]  # x
        edge_src_y = graph_x.nodes.get(edge_src)['pos'][1]  # y
        edge_dest_x = graph_x.nodes.get(edge_dest)['pos'][0]  # x
        edge_dest_y = graph_x.nodes.get(edge_dest)['pos'][1]  # y
        dist_src_edge = math.sqrt((edge_src_x - edge_dest_x) ** 2 + ((edge_src_y - edge_dest_y) ** 2))
        dist_src_n = math.sqrt((edge_src_x - pokemon_id_src_x) ** 2 + ((edge_src_y - pokemon_id_src_y) ** 2))
        dist_n_dest = math.sqrt((pokemon_id_src_x - edge_dest_x) ** 2 + ((pokemon_id_src_y - edge_dest_y) ** 2))
        if abs(dist_src_edge - (dist_src_n + dist_n_dest)) < EPS:
            if graph_x.nodes[pokemon_id]['type'] > 0:  # if type == 1
                return min(edge_src, edge_dest) , max(edge_src, edge_dest)
            else:
                return max(edge_src, edge_dest) , min(edge_src, edge_dest)

        """
        find if there is a free agent 
        @param agents: list of agents
        @return: the id of the free agent , if there is no free agent returns -1   
        """
def find_free_agent(agents):
    for agent in agents:
        if (agent.dest == -1):  # maybe "agent.dest" .. think its the same..
            agent.dest=1
            return (agent.id+1000)
    # if we didnt find a free agent.
    return -1



"""
        find if there is a free agent 
        @param agent_id: list of agents
        @param p_edge_src: src of the pokemon's edge  
        @param p_edge_dest: dest of the pokemon's edge  
        @return: the id of the ideal agent and the idial path 
        Note: 
"""
def find_agent_edge(agent_id):
    agent_id_src_x = graph_x.nodes.get(agent_id)['pos'][0]  # x
    agent_id_src_y = graph_x.nodes.get(agent_id)['pos'][1]  # y

    for edge in list(graph_x.edges):
        edge_src = edge[0]  # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x.nodes.get(edge_src)['pos'][0]  # x
        edge_src_y = graph_x.nodes.get(edge_src)['pos'][1]  # y
        edge_dest_x = graph_x.nodes.get(edge_dest)['pos'][0]  # x
        edge_dest_y = graph_x.nodes.get(edge_dest)['pos'][1]  # y
        dist_src_edge = math.sqrt((edge_src_x - edge_dest_x) ** 2 + ((edge_src_y - edge_dest_y) ** 2))
        dist_src_n = math.sqrt((edge_src_x - agent_id_src_x) ** 2 + ((edge_src_y - agent_id_src_y) ** 2))
        dist_n_dest = math.sqrt((agent_id_src_x - edge_dest_x) ** 2 + ((agent_id_src_y - edge_dest_y) ** 2))
        if abs(dist_src_edge - (dist_src_n + dist_n_dest)) < EPS:
            # if n.type > 0: # if type == 1
            return edge_src, edge_dest

"""
        find the path that agent need to reach 
        @param agent_id : id of the agent
        @param p_src: src of the pokemon's edge  
        @param p_dest: dest of the pokemon's edge  
        @return:list that represent the path that agent need to reach 
        Note: 
"""
def get_agent_path(agent_id, p_src, p_dest):
    path = nx.shortest_path(graph_x, agents[agent_id].src, p_dest)
    contained = 0
    for p in path:
        if (p == p_src):
            contained = 1
    if (contained == 0):
        path.insert(len(path), p_src)
        path.insert(len(path), p_dest)
    return path

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



"""
*************************************************************** GUI **********************************************8
"""
def arrow(start, end, d, h, color):

    dx =(end[0] - start[0])
    dy =(end[1] - start[1])
    D = (math.sqrt(dx * dx + dy * dy))
    xm =(D - d)
    xn =(xm)
    ym =(h)
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

    pygame.draw.line(screen, color, start, end, width=2)
    pygame.draw.polygon(screen, color, points)
class Button:
    def __init__(self,rect:pygame.Rect,text:str,color,func=None):
        self.rect=rect
        self.text=text
        self.color=color
        self.func=func
        self.is_pressed=False
    def press(self):
        self.is_pressed = not self.is_pressed
class NodeScreen:
    def __init__(self,rect:pygame.Rect,id):
        self.rect=rect
        self.id=id
button_exit =Button(pygame.Rect((0,0),(120,30)),"Exit button",(255,255,0))
button_countdown =Button(pygame.Rect((120,0),(160,30)),"countdown",(255,0,0))
button_grade =Button(pygame.Rect((0,30),(120,30)),"grade",(0,255,0))
button_level =Button(pygame.Rect((120,30),(160,30)),"level",(0,128,230))

result=[]
node_screens=[]
def on_click(func):
    global result
    result=func()
"""
*************************************************************** GUI **********************************************8
"""
def put_agent_on_graph():
    num_of_agent = client.get_info()
    num_of_agent = num_of_agent.partition("agents")[2]
    num_of_agent = num_of_agent.replace("\"", '')
    num_of_agent = num_of_agent.replace(':', '')
    num_of_agent = num_of_agent.replace("}", '')
    num_of_agent = int(num_of_agent)
    for i in range(num_of_agent):
        client.add_agent('{\"id\":' + str(i) + '}')

def get_grade():
    grade = client.get_info()
    grade = grade.partition("grade")[2]
    grade = grade.split(",")
    grade = grade[0]
    grade = grade.replace("\"", '')
    grade = grade.replace(':', '')
    grade = grade.replace("}", '')
    grade = int(grade)
    return grade

def get_game_level():
    level = client.get_info()
    level = level.partition("level")[2]
    level = level.split(",")
    level = level[0]
    level = level.replace("\"", '')
    level = level.replace(':', '')
    level = level.replace("}", '')
    level = int(level)
    return level

put_agent_on_graph()

# this commnad starts the server - the game is running now
client.start()

while client.is_running() == 'true':


    """
    i add in here graph algo so we load_json to the graph_algo and then we get all the nodes to be added to the 
    graph_x
    """
    graph_x = nx.DiGraph()
    graph_algo = GraphAlgo()
    graph_algo.load_from_json_3(graph)
    for n in graph_algo.get_graph().get_all_v().keys():
        node: Node = graph_algo.get_graph().get_all_v().get(n)
        graph_x.add_node(node.get_key(), pos=(node.get_x(), node.get_y()), value=0, type=0)
        for dest_id, weight, in graph_algo.get_graph().all_out_edges_of_node(node.get_key()).items():
            graph_x.add_edge(node.get_key(), dest_id, weight=weight)
    graph_x.add_node(999, pos=(35.188900353135324,
                               32.105320110855615))  ############################3 NOTICE THAT THIS NODE IS ADDED FOR TEST THE FUCNTION 'find_pokemon_edge_test'
    pokemons = json.loads(client.get_pokemons(),object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in (pokemons)]


    """
    i add in here the pokemon to graph algo and i gave an id to them start from 2000
    """
    p_id = 1999
    for p in (pokemons):
        p_id=p_id+1
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=float(x), y=float(y))
        graph_x.add_node(p_id, pos=(p.pos.x, p.pos.y), value=p.value, type=p.type, status='free')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))


    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    """
    i add in here the agent to graph algo and i gave an id to them start from 1000
    """
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=float(x), y=float(y))
        graph_x.add_node(a.id + 1000, pos=(a.pos.x, a.pos.y), value=a.value, src=a.src, dest=a.dest, speed=a.speed)
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    pos = nx.get_node_attributes(graph_x, 'pos')
    nx.draw(graph_x, pos, with_labels=True)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_exit.rect.collidepoint(event.pos):
                client.stop_connection()

    IMAGE_SCREEN_BACKGROUND = pygame.image.load("pica.jpg")
    IMAGE_POKEMON_SCALE = pygame.transform.scale(IMAGE_SCREEN_BACKGROUND, (screen.get_width(),screen.get_height()))
    screen.blit(IMAGE_POKEMON_SCALE,(0,0))

    """
    button
    """
    grade = get_grade()
    level = get_game_level()
    time_to_end = client.time_to_end()

    # game_level =
    pygame.draw.rect(screen,button_exit.color,button_exit.rect)
    pygame.draw.rect(screen,button_countdown.color,button_countdown.rect)
    pygame.draw.rect(screen,button_grade.color,button_grade.rect)
    pygame.draw.rect(screen,button_level.color,button_level.rect)

    # if button.is_pressed:
    button_exit_text=FONT.render(button_exit.text,True,(0,0,0))
    button_countdown_text=FONT.render(f"countdown: {time_to_end}",True,(0,0,0))
    button_grade_text=FONT.render(f"grade: {grade}",True,(0,0,0))
    button_level_text=FONT.render(f"level: {level}",True,(0,0,0))
    screen.blit(button_exit_text,(button_exit.rect.x+15,button_exit.rect.y+5))
    screen.blit(button_countdown_text,(button_countdown.rect.x+12,button_countdown.rect.y+5))
    screen.blit(button_grade_text,(button_grade.rect.x+15,button_grade.rect.y+5))
    screen.blit(button_level_text,(button_level.rect.x+12,button_level.rect.y+5))


    IMAGE_WIDTH, IMAGE_HEIGHT = 55,40
    IMAGE_POKEMON = pygame.image.load("pokemon_image.png")
    IMAGE_POKEMON_SCALE = pygame.transform.scale(IMAGE_POKEMON, (IMAGE_WIDTH,IMAGE_HEIGHT))
    IMAGE_AGENT = pygame.image.load("pokeball-png.png")
    IMAGE_AGENT_SCALE = pygame.transform.scale(IMAGE_AGENT, (IMAGE_WIDTH,IMAGE_HEIGHT))

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

        arrow((src_x, src_y), (dest_x, dest_y), 27, 10, color=(255, 0, 0))


    # draw nodes
    for n in graph.Nodes:

        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw agents
    zip_agent_pokemon = zip(agents, pokemons)

    for agent, p in zip_agent_pokemon:
        screen.blit(IMAGE_AGENT_SCALE,(int(agent.pos.x-20), int(agent.pos.y-20)))
        screen.blit(IMAGE_POKEMON_SCALE,(int(p.pos.x-20), int(p.pos.y-20)))
    display.update()

    # refresh rate
    clock.tick(60)


    for n in graph_x.nodes:
        if n < 1000:  # if the node is a node in the graph - continue
            continue
        if n >= 2000:  # if p in an  pokemon
            p_src, p_dest = find_pokemon_edge_test(n)
            free_agent_id = find_free_agent(agents)
            if (free_agent_id != -1):  # if we have found a free agent
                a_path = get_agent_path((free_agent_id-1000), p_src, p_dest)
                if (bool(call.get(n))):
                    if (call.get(n) == int (free_agent_id)):
                        client.choose_next_edge('{"agent_id":' + str((call[n]-1000)) + ', "next_node_id":' + str(a_path[1]) + '}')
                        ttl = client.time_to_end()
                        print(ttl, client.get_info())
                    else:
                        continue
                else:
                    call[n] = int (free_agent_id)
                    client.choose_next_edge('{"agent_id":' + str((free_agent_id-1000)) + ', "next_node_id":' + str(a_path[1]) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())
            else:
                if (bool(call.get(n))):
                    ag = call.get(n)
                    a_path=get_agent_path((ag-1000), p_src, p_dest)
                    client.choose_next_edge('{"agent_id":' + str((call[n] - 1000)) + ', "next_node_id":' + str(a_path[1]) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())
    client.move()
# game over: