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
        draw_rectangle(*self.get_bb(), 0, 0, 255)

    def get_bb(self):
        return (self.x - 100 + (self.dir * 30), self.y - 50, self.x + 100 + (self.dir * 30), self.y + 50)

    def handle_collision(self, group, other):
        pass