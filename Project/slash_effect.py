from pico2d import load_image
import game_world

class SlashEffect:
    image = None
    def __init__(self, x = 0, y = 0, spead = 10):
        if SlashEffect.image is None:
            SlashEffect.image = load_image('Sprite/Player_skill_effect.png')
        self.x, self.y = x, y
        self.spead = spead
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2
        self.x += self.spead
        if self.x < -64 or self.x > 1280 + 64:
            game_world.remove_object(self)

    def draw(self):
        if self.spead > 0:
            self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y, 128, 128)
        else:
            self.image.clip_composite_draw(self.frame * 64, 0, 64, 64, 0, 'h', self.x, self.y, 128, 128)