import json
import os
from types import SimpleNamespace
import pygame
from pygame import Color, display, gfxdraw
from pygame.constants import RESIZABLE

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption("Pokemon Game!")
COLOR = (255,255,255)
FramePerSec = 60

## =========== put graph for check ========================
with open('A0.json', 'r') as file:
    graph = json.load(
        file, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
## =========== put graph for check ========================

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# get data proportions

min_x = min(list(graph.nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.nodes), key=lambda n: n.pos.y).pos.y



def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15
def draw_window():
    WIN.fill(COLOR)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FramePerSec)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == '__main__':
    main()