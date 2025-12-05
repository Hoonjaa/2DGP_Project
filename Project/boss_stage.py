from pico2d import *
import game_world
import game_framework
import common
import forge_ui_stage
from player_ui import PlayerUI
from player import Player
from castle_ground import CastleGround
from castle_background import CastleBackground
from boss import Boss
import death_stage

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(forge_ui_stage)
        else:
            common.player.handle_event(event)

def init():
    common.is_scrolling = False

    background = CastleBackground()
    game_world.add_object(background,0)

    ground = CastleGround()
    game_world.add_object(ground,0)

    if common.player is None:
        common.player = Player()
    common.player.x = 100
    game_world.add_object(common.player,1)
    game_world.add_collision_pair('player:monster_attack', common.player, None)
    game_world.add_collision_pair('player:jewel', common.player, None)

    player_ui = PlayerUI(common.player)
    game_world.add_object(player_ui,3)

    boss = Boss()
    boss.x = 1000
    game_world.add_object(boss, 0)
    game_world.add_collision_pair('monster:player_attack', boss, None)
    game_world.add_collision_pair('monster:player_slash', boss, None)
    game_world.add_collision_pair('monster:player_ult', boss, None)

def update():
    game_world.update()
    game_world.handle_collisions()

    if common.player.hp <= 0:
        common.player.hp = common.player.max_hp
        game_framework.change_mode(death_stage)

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