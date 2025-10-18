from pico2d import *

def reset_world():
    global world

    world = []

def update_world():
    pass

def render_world():
    clear_canvas()
    update_canvas()



running = True

open_canvas(1280, 720)
reset_world()

while running:
    update_world()
    render_world()
    delay(0.01)

close_canvas()