from pico2d import *
import random
import game_world
import game_framework
import common
from player_ui import PlayerUI
from brute import Brute
from player import Player
from zombie import Zombie
from variant_zombie2 import VZ2
from variant_zombie1 import VZ1
from boss import Boss
from scroll_blue_sky import ScrollBlueSky
from scroll_ground_1 import ScrollGround1


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.player.handle_event(event)

def init():
    common.is_scrolling = True

    common.sky_1 = ScrollBlueSky()
    game_world.add_object(common.sky_1,0)

    common.ground_1 = ScrollGround1()
    game_world.add_object(common.ground_1,0)

    if common.player is None:
        common.player = Player()
    common.player.x = 100
    game_world.add_object(common.player,1)
    game_world.add_collision_pair('player:monster_attack', common.player, None)

    player_ui = PlayerUI(common.player)
    game_world.add_object(player_ui,3)

    for _ in range(20):
        zombie = Brute()
        zombie.x = random.randint(500, 7000)
        game_world.add_object(zombie, 0)
        # game_world.add_collision_pair('player:monster_attack', None, zombie)
        game_world.add_collision_pair('monster:player_attack', zombie, None)
        game_world.add_collision_pair('monster:player_slash', zombie, None)
        game_world.add_collision_pair('monster:player_ult', zombie, None)

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