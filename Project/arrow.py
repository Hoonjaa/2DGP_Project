from pico2d import *
import game_world

class Arrow:
    def __init__(self, x, y):
        self.image = load_image('Sprite/navigation_s.png')
        self.x = x
        self.y = y

    def draw(self, x, y):
        self.image.draw(x, y)

    def update(self):
        pass

    def change_position(self, x, y):
        self.x = x
        self.y = y