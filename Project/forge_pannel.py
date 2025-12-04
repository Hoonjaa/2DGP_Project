from pico2d import *
import game_world
from arrow import Arrow

class ForgePannel:
    def __init__(self):
        self.image = load_image('Sprite/forge_ui.png')
        self.arrow_positions = ((200, 500), (400, 500), (600, 500), (800, 500)) # 임시값
        self.arrow = Arrow(*self.arrow_positions[0])
        game_world.add_object(self.arrow,3)

    def draw(self):
        self.image.draw(640, 360)

    def update(self):
        pass

    def handle_event(self, event):
        pass