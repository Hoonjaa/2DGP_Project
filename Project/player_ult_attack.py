from pico2d import draw_rectangle

class PlayerUltAttack:
    def __init__(self, x = 0, y = 0, player = None):
        self.player = player
        self.x, self.y = x + (140 * self.player.face_dir), y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb(), 0, 255, 0)

    def get_bb(self):
        return (self.x - 200, self.y - 50, self.x + 200, self.y + 100)

    def handle_collision(self, group, other):
        pass