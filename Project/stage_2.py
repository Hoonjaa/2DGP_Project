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
from scroll_red_sky import ScrollRedSky
from scroll_ground_1 import ScrollGround1
import stage_3


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
    common.total_monster = 29

    common.sky_1 = ScrollRedSky()
    game_world.add_object(common.sky_1,0)

    common.ground_1 = ScrollGround1()
    game_world.add_object(common.ground_1,0)

    if common.player is None:
        common.player = Player()
    common.player.x = 100
    game_world.add_object(common.player,1)
    game_world.add_collision_pair('player:monster_attack', common.player, None)
    game_world.add_collision_pair('player:jewel', common.player, None)

    player_ui = PlayerUI(common.player)
    game_world.add_object(player_ui,3)

    for _ in range(8):
        zombie = Zombie()
        zombie.x = random.randint(500, 7000)
        game_world.add_object(zombie, 0)
        game_world.add_collision_pair('player:monster_attack', None, zombie)
        game_world.add_collision_pair('monster:player_attack', zombie, None)
        game_world.add_collision_pair('monster:player_slash', zombie, None)
        game_world.add_collision_pair('monster:player_ult', zombie, None)

    for _ in range(15):
        vz2 = VZ2()
        vz2.x = random.randint(1000, 7000)
        game_world.add_object(vz2, 0)
        game_world.add_collision_pair('player:monster_attack', None, vz2)
        game_world.add_collision_pair('monster:player_attack', vz2, None)
        game_world.add_collision_pair('monster:player_slash', vz2, None)
        game_world.add_collision_pair('monster:player_ult', vz2, None)

    for _ in range(5):
        brute = Brute()
        brute.x = random.randint(3000, 7000)
        game_world.add_object(brute, 0)
        game_world.add_collision_pair('monster:player_attack', brute, None)
        game_world.add_collision_pair('monster:player_slash', brute, None)
        game_world.add_collision_pair('monster:player_ult', brute, None)

    for _ in range(1):
        vz1 = VZ1()
        vz1.x = random.randint(5000, 7000)
        game_world.add_object(vz1, 0)
        game_world.add_collision_pair('monster:player_attack', vz1, None)
        game_world.add_collision_pair('monster:player_slash', vz1, None)
        game_world.add_collision_pair('monster:player_ult', vz1, None)

def update():
    game_world.update()
    game_world.handle_collisions()

    if common.player.x > 7600 and common.total_monster <= 0:
        game_framework.change_mode(stage_3)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    if common.ground_1:
        common.ground_1.stop_bgm()
    game_world.clear()

def pause():
    pass

def resume():
    pass