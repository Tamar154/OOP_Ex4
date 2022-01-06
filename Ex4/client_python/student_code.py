"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import json
from math import sqrt
import sys
from types import SimpleNamespace

import pygame

from pygame import *
from pygame import gfxdraw

from client_python.GraphAlgo import GraphAlgo
from client_python.client import Client

pygame.font.init()

import time

EPSILON = 0.3
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
pygame.display.set_caption("Pokemon game")
player = pygame.image.load("player.png")
pikachu = pygame.image.load("pikachu.png")
snorlax = pygame.image.load("snorlax.png")
icon = pygame.image.load("pokeball.png")
Exit = pygame.image.load("exit.png").convert_alpha()
Pause = pygame.image.load("pause.png").convert_alpha()
pygame.display.set_icon(icon)
pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)
graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

# temp = json.loads(
#     graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
temp = json.loads(graph_json)
graph_algo = GraphAlgo()
with open('temp.json', 'w') as f:
    json.dump(temp, f)

graph_algo.load_from_json("temp.json")
graph = graph_algo.graph

for n in graph.nodes.values():
    x = n.get_x()
    y = n.get_y()
    # x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.nodes.values()), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.nodes.values()), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.nodes.values()), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.nodes.values()), key=lambda n: n.pos.y).pos.y


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


# Adds Exit and Pause Buttons xp1 and yp1 is x and y pimage is image
class Button:
    def __init__(self, xp1, yp1, pimage):
        # self.yp1 = yp1
        # self.xp1 = xp1
        self.image = pimage
        self.rect = self.image.get_rect()
        # self.rect.topright(xp1, yp1)
        self.rect.x = xp1
        self.rect.y = yp1
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # checking mouse and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw the button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create button instances
Exit_button = Button(0, 0, Exit)
Pause_button = Button(75, 0, Pause)

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
counter = 0
# show timer on screen
timer_font = pygame.font.SysFont('comicsans', 30)

# bp = pygame.image.load("b1.jpg").convert()
# bp = pygame.image.load("b2.jpg").convert()
bp = pygame.image.load("b3.jpg").convert()
picked_agent=0
while client.is_running() == 'true':

    start = int(client.time_to_end())
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

    # refresh surface and add Background and buttons
    screen.fill(Color(0, 0, 0))
    screen.blit(bp, (-425, -200))
    timer_text = timer_font.render("Time: " + str(int(client.time_to_end())/1000), True, (255,215,0))
    screen.blit(timer_text,(150,0))
    # need to add pause action to the game
    Pause_button.draw()
    if Exit_button.draw():
        pygame.quit()

    # draw nodes
    for n in graph.nodes.values():
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(255, 255, 255))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(0, 0, 0))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 0, 0))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for i in graph.edges.values():
        for j in i.values():
            edge = j
            # find the edge nodes
            src = next(n for n in graph.nodes.values() if n.id == edge.src)
            dest = next(n for n in graph.nodes.values() if n.id == edge.dest)

            # scaled positions
            src_x = my_scale(src.pos.x, x=True)
            src_y = my_scale(src.pos.y, y=True)
            dest_x = my_scale(dest.pos.x, x=True)
            dest_y = my_scale(dest.pos.y, y=True)

            # draw the line
            pygame.draw.line(screen, Color(240, 220, 130),
                             (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        # pygame.draw.circle(screen, Color(122, 61, 23),
        #                    (int(agent.pos.x), int(agent.pos.y)), 10)
        #
        screen.blit(player, (agent.pos.x, agent.pos.y))
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        if p.pos.x < p.pos.y:
            # pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
            screen.blit(pikachu, (p.pos.x, p.pos.y))
        else:
            # pygame.draw.circle(screen, Color(139, 0, 0), (int(p.pos.x), int(p.pos.y)), 10)
            screen.blit(snorlax, (p.pos.x, p.pos.y))

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    pokemons_dict = {}
    agents_dict = {}

    for pokemon in pokemons:
        for i in graph.edges.values():
            for j in i.values():
                edge = j
                x1, x2, x3 = graph.nodes.get(edge.src).pos.x, graph.nodes.get(edge.dest).pos.x, pokemon.pos.x
                y1, y2, y3 = graph.nodes.get(edge.src).pos.y, graph.nodes.get(edge.dest).pos.y, pokemon.pos.y
                x1 = my_scale(x1, x=True)
                x2 = my_scale(x2, x=True)
                y1 = my_scale(y1, y=True)
                y2 = my_scale(y2, y=True)
                AB = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
                AP = sqrt((x3 - x1) * (x3 - x1) + (y3 - y1) * (y3 - y1))
                PB = sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
                # if AB + AP - PB < EPSILON:
                if abs(AP + PB - AB) < EPSILON:
                    pokemons_dict[edge.get_src()] = edge
                    # client.move()
                    # time.sleep(time.thread_time()/15)

    minimum = sys.float_info.max
    path = []
    picked_agent = agents[0]
    temp_path = []
    for pokemon in pokemons_dict.values():
        for agent in agents:
            if agent.dest == -1:
                temp_dest, temp_path = graph_algo.shortest_path(agent.src, pokemon.get_src())  # dest?
                temp_path.append(pokemon.get_dest())
                if temp_dest < minimum:
                    minimum = temp_dest
                    path = temp_path
                    picked_agent = agent

    for i in temp_path:
        if picked_agent.dest == -1:
            client.choose_next_edge('{"agent_id":' + str(picked_agent.id) + ', "next_node_id":' + str(i) + '}')


        # client.choose_next_edge(
        #     '{"agent_id":' + str(picked_agent.id) + ', "next_node_id":' + str(10) + '}')
    # if picked_agent.dest != -1:
    #     client.move()

    # end = time.time()
    # if (start - int(client.time_to_end())) < 1000 and counter >= 10:
    #     start = int(client.time_to_end())
    #     counter = 0
    # else:
    #     client.move()
    #     counter += 1

    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.nodes)
    #         client.choose_next_edge(
    #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
    #         ttl = client.time_to_end()
    #         print(ttl, client.get_info())
    # if picked_agent.dest != -1:
    #     client.move()

# game over:
