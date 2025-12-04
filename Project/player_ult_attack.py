from pico2d import draw_rectangle
import common

class PlayerUltAttack:
    def __init__(self, x = 0, y = 0, player = None):
        self.player = player
        self.x, self.y = x + (140 * self.player.face_dir), y

    def update(self):
        self.x = self.player.x + (140 * self.player.face_dir)
        self.y = self.player.y

    def draw(self):
        draw_rectangle(*self.get_bb(), 0, 255, 0)

    def get_bb(self):
        if common.is_scrolling:
            sx = self.x - common.sky_1.window_left
            sy = self.y - common.sky_1.window_bottom
            return (sx - 200, sy - 50, sx + 200, sy + 100)
        else:
            return (self.x - 200, self.y - 50, self.x + 200, self.y + 100)

    def handle_collision(self, group, other):
        pass