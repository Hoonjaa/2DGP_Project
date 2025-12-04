from pico2d import *
import game_world
import game_framework
import common
import forge_ui_stage
import stage_1
from player_ui import PlayerUI
from player import Player
from forge_ground import ForgeGround
from blue_sky import BlueSky
from scroll_blue_sky import ScrollBlueSky
from forge import Forge

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

    sky = BlueSky()
    game_world.add_object(sky,0)

    ground = ForgeGround()
    game_world.add_object(ground,0)

    forge = Forge()
    game_world.add_object(forge,0)

    if common.player is None:
        common.player = Player()
    game_world.add_object(common.player,1)

    player_ui = PlayerUI(common.player)
    game_world.add_object(player_ui,3)

def update():
    game_world.update()
    game_world.handle_collisions()

    if common.player.x > 1270:
        game_framework.change_mode(stage_1)

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