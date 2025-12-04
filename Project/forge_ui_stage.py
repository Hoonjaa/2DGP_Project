from pico2d import *
import game_framework
import game_world
from forge_pannel import ForgePannel

forge_pannel = None

def pause():
    pass

def resume():
    pass

def init():
    global forge_pannel
    forge_pannel = ForgePannel()
    game_world.add_object(forge_pannel,3)

def finish():
    game_world.remove_object(forge_pannel.arrow)
    game_world.remove_object(forge_pannel)

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    # flush input
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        else:
            forge_pannel.handle_event(event)