from pico2d import *
import game_framework
import first_stage

image = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(first_stage)

def pause():
    pass

def resume():
    pass

def init():
    global image

    image = load_image('Sprite/title_image.png')

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.clip_draw(0,0,1344,768,640,360)
    update_canvas()
