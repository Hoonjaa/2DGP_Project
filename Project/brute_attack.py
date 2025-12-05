from pico2d import draw_rectangle
import common

class BruteAttack:
    def __init__(self, x = 0, y = 0, damage = 0, brute = None):
        self.attack_damage = damage
        self.brute = brute
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        # draw_rectangle(*self.get_bb(), 0, 0, 255)
        pass

    def get_bb(self):
        if common.is_scrolling:
            screen_x = self.x - common.ground_1.window_left
            screen_y = self.y - common.ground_1.window_bottom
            return (screen_x - 180, screen_y - 130, screen_x + 180, screen_y + 130)
        else:
            return (self.x - 180, self.y - 130, self.x + 180, self.y + 130)

    def handle_collision(self, group, other):
        pass