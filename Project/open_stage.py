from pico2d import *
import game_framework
import game_world

timer = 1.0
alpha = 255
black_screen = None

def pause():
    pass

def resume():
    pass

def init():
    global black_screen
    black_screen = load_image('Sprite/black_screen.png')

def finish():
    pass

def update():
    global timer, alpha
    timer -= game_framework.frame_time
    alpha = max(0, alpha - 255 * game_framework.frame_time)
    if timer < 0:
        game_framework.pop_mode()

def draw():
    clear_canvas()
    game_world.render()

    black_screen.opacify(alpha / 255.0)
    black_screen.draw(640, 360)

    update_canvas()

def handle_events():
    # flush input
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()