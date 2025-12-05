from pico2d import draw_rectangle

class BossAttack:
    def __init__(self, x = 0, y = 0, damage = 0, dir = 0, boss_attack = None):
        self.attack_damage = damage
        self.dir = dir
        self.boss_attack = boss_attack
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        # draw_rectangle(*self.get_bb(), 0, 0, 255)
        pass

    def get_bb(self):
        return (self.x - 140 + (self.dir * 50), self.y - 60, self.x + 140 + (self.dir * 50), self.y + 200)

    def handle_collision(self, group, other):
        pass