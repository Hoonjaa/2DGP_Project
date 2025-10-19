from pico2d import *
from player import Player
from test_background import Background

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def reset_world():
    global world
    global player

    world = []

    background = Background()
    world.append(background)

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
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()