from pico2d import *
import common

class Jewel:
    def __init__(self, x = 0, y = 0, price = 0):
        self.x, self.y = x, 60
        self.price = price
        self.image = load_image('Sprite/jewel.png')

    def update(self):
        pass

    def draw(self):
        sx = self.x - common.ground_1.window_left
        sy = self.y - common.ground_1.window_bottom
        self.image.clip_draw(0, 0, 80, 80, sx, sy, 40, 40)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        screen_x = self.x - common.ground_1.window_left
        screen_y = self.y - common.ground_1.window_bottom
        return (screen_x - 20, screen_y - 20, screen_x + 20, screen_y + 20)

    def handle_collision(self, group, other):
        pass