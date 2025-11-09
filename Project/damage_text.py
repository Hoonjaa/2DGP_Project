from pico2d import load_font
import game_world
import game_framework

class DamageText:
    font = None
    def __init__(self, x = 0, y = 0, damage = 0):
        self.x, self.y = x, y
        self.damage = damage
        if DamageText.font == None:
            DamageText.font = load_font('ENCR10B.TTF', 20)
        self.timer = 1.0

    def update(self):
        self.timer -= game_framework.frame_time
        self.y += 30 * game_framework.frame_time

        if self.timer <= 0:
            game_world.remove_object(self)

    def draw(self):
        DamageText.font.draw(self.x, self.y, str(self.damage), (255, 0, 0))