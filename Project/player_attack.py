from pico2d import draw_rectangle
import common

class PlayerAttack:
    def __init__(self, x = 0, y = 0, player = None):
        self.player = player
        self.x, self.y = x, y

    def update(self):
        self.x = self.player.x
        self.y = self.player.y

    def draw(self):
        draw_rectangle(*self.get_bb(), 0, 255, 0)

    def get_bb(self):
        if common.is_scrolling:
            sx = self.x - common.sky_1.window_left
            sy = self.y - common.sky_1.window_bottom
            return (sx - 100, sy - 50, sx + 100, sy + 100)
        else:
            return (self.x - 100, self.y - 50, self.x + 100, self.y + 100)

    def handle_collision(self, group, other):
        pass