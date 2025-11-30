from pico2d import load_image

class ForgeGround:
    def __init__(self):
        self.image = load_image('Sprite/ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640,360, 1280, 720)