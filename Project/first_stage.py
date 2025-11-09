from pico2d import *
import game_world
import game_framework
from player import Player
from zombie import Zombie
from test_background import Background

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global player

    background = Background()
    game_world.add_object(background,0)

    player = Player()
    game_world.add_object(player,1)

    zombie = Zombie()
    game_world.add_object(zombie,0)
    game_world.add_collision_pair('zombie:player_attack', zombie, None)
    game_world.add_collision_pair('zombie:player_slash', zombie, None)
    game_world.add_collision_pair('zombie:player_ult', zombie, None)

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass