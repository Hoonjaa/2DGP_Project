from pico2d import load_image, load_music

class CastleBackground:
    def __init__(self):
        self.image = load_image('Sprite/castle.png')
        self.bgm = load_music('Sound/boss.mp3')
        self.bgm.set_volume(25)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(640,360, 1280, 720)