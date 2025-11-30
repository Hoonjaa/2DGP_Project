from pico2d import *
import game_framework
import first_stage

image = None
logo_start_time = 2.0

def pause():
    pass

def resume():
    pass

def init():
    global image, logo_start_time

    image = load_image('Sprite/tuk_credit.png')

def finish():
    global image
    del image

def update():
    # logo 모드가 2초간 지속되도록 한다.
    global logo_start_time

    logo_start_time -= game_framework.frame_time
    if logo_start_time <= 0.0:
        game_framework.change_mode(first_stage)

def draw():
    clear_canvas()
    image.clip_draw(0,0,800,600,640,360,1600,1200)
    update_canvas()

def handle_events():
    # flush input
    events = get_events()