from pico2d import *
import game_world
import game_framework
from player_ui import PlayerUI
from brute import Brute
from player import Player
from zombie import Zombie
from variant_zombie2 import VZ2
from variant_zombie1 import VZ1
from boss import Boss
from test_background import Background

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            zombie = Zombie()
            game_world.add_object(zombie, 0)
            game_world.add_collision_pair('player:monster_attack', None, zombie)
            game_world.add_collision_pair('monster:player_attack', zombie, None)
            game_world.add_collision_pair('monster:player_slash', zombie, None)
            game_world.add_collision_pair('monster:player_ult', zombie, None)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            brute = Brute()
            game_world.add_object(brute, 0)
            game_world.add_collision_pair('monster:player_attack', brute, None)
            game_world.add_collision_pair('monster:player_slash', brute, None)
            game_world.add_collision_pair('monster:player_ult', brute, None)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            vz2 = VZ2()
            game_world.add_object(vz2, 0)
            game_world.add_collision_pair('player:monster_attack', None, vz2)
            game_world.add_collision_pair('monster:player_attack', vz2, None)
            game_world.add_collision_pair('monster:player_slash', vz2, None)
            game_world.add_collision_pair('monster:player_ult', vz2, None)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            vz1 = VZ1()
            game_world.add_object(vz1, 0)
            game_world.add_collision_pair('monster:player_attack', vz1, None)
            game_world.add_collision_pair('monster:player_slash', vz1, None)
            game_world.add_collision_pair('monster:player_ult', vz1, None)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            boss = Boss()
            game_world.add_object(boss, 0)
            game_world.add_collision_pair('monster:player_attack', boss, None)
            game_world.add_collision_pair('monster:player_slash', boss, None)
            game_world.add_collision_pair('monster:player_ult', boss, None)
        else:
            player.handle_event(event)

def init():
    global player

    background = Background()
    game_world.add_object(background,0)

    player = Player()
    game_world.add_object(player,1)
    game_world.add_collision_pair('player:monster_attack', player, None)

    player_ui = PlayerUI(player)
    game_world.add_object(player_ui,3)

    # zombie = Zombie()
    # game_world.add_object(zombie,0)
    # game_world.add_collision_pair('player:monster_attack', None, zombie)
    # game_world.add_collision_pair('monster:player_attack', zombie, None)
    # game_world.add_collision_pair('monster:player_slash', zombie, None)
    # game_world.add_collision_pair('monster:player_ult', zombie, None)
    #
    # brute = Brute()
    # game_world.add_object(brute,0)
    # game_world.add_collision_pair('monster:player_attack', brute, None)
    # game_world.add_collision_pair('monster:player_slash', brute, None)
    # game_world.add_collision_pair('monster:player_ult', brute, None)
    #
    # vz2 = VZ2()
    # game_world.add_object(vz2,0)
    # game_world.add_collision_pair('player:monster_attack', None, vz2)
    # game_world.add_collision_pair('monster:player_attack', vz2, None)
    # game_world.add_collision_pair('monster:player_slash', vz2, None)
    # game_world.add_collision_pair('monster:player_ult', vz2, None)
    #
    # vz1 = VZ1()
    # game_world.add_object(vz1,0)
    # game_world.add_collision_pair('monster:player_attack', vz1, None)
    # game_world.add_collision_pair('monster:player_slash', vz1, None)
    # game_world.add_collision_pair('monster:player_ult', vz1, None)
    #
    # boss = Boss()
    # game_world.add_object(boss,0)

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