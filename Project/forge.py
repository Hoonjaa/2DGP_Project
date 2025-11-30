from pico2d import load_image
import game_framework

class Forge:
    def __init__(self):
        self.image = load_image('Sprite/forge.png')
        self.frame = 0
        self.anim_progress = 0.0

    def update(self):
        self.anim_progress += 2.0 * game_framework.frame_time * 4
        self.frame = int(self.anim_progress) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 240, 0, 240, 210, 640, 350, 720, 630)