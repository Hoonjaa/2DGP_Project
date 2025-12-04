from pico2d import draw_rectangle
import common

class VZ2Attack:
    def __init__(self, x = 0, y = 0, damage = 0, dir = 0, vz2 = None):
        self.attack_damage = damage
        self.dir = dir
        self.vz2 = vz2
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb(), 0, 0, 255)

    def get_bb(self):
        if common.is_scrolling:
            screen_x = self.x - common.ground_1.window_left
            screen_y = self.y - common.ground_1.window_bottom
            return (screen_x - 100 + (self.dir * 30), screen_y - 50, screen_x + 100 + (self.dir * 30), screen_y + 50)
        else:
            return (self.x - 100 + (self.dir * 30), self.y - 50, self.x + 100 + (self.dir * 30), self.y + 50)

    def handle_collision(self, group, other):
        pass