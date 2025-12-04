from pico2d import *

class ForgePannel:
    def __init__(self):
        self.image = load_image('Sprite/forge_ui.png')

    def draw(self):
        self.image.draw(640, 360)

    def update(self):
        pass