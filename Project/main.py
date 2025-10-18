from pico2d import *
from player import Player

def reset_world():
    global world

    world = []

    player = Player()
    world.append(player)

def update_world():
    for obj in world:
        obj.update()

def render_world():
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()



running = True

open_canvas(1280, 720)
reset_world()

while running:
    update_world()
    render_world()
    delay(0.1)

close_canvas()