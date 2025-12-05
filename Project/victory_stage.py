from pico2d import *
import game_framework

image = None
sound = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.quit()

def pause():
    pass

def resume():
    pass

def init():
    global image, sound

    image = load_image('Sprite/victory.png')
    sound = load_music('Sound/victory.mp3')
    sound.set_volume(32)
    sound.play()

def finish():
    global image, sound
    del image
    if sound:
        sound.stop()

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640,360,1280,720)
    update_canvas()
