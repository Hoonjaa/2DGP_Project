from pico2d import load_image, draw_rectangle
import game_world
import game_framework

class BossSkill:
    def __init__(self, x = 0, y = 0, damage = 0, dir = 0, boss_attack = None):
        self.image = load_image('Sprite/reaper_skill_effect.png')
        self.attack_damage = damage
        self.dir = dir
        self.boss_attack = boss_attack
        self.x, self.y = x, y

        self.width = 1024
        self.height = 256
        self.d_width = 102
        self.d_height = 25
        self.count = 1

        self.count_cooldown = 0.3
        self.count_cool_time = 0.3

    def update(self):
        if self.count_cooldown > 0:
            self.count_cooldown -= game_framework.frame_time
            if self.count_cooldown < 0:
                self.count_cooldown = self.count_cool_time
                self.count += 1

    def draw(self):
        size_x, size_y = self.width - self.count * self.d_width, self.height - self.count * self.d_height
        if self.dir == 1:
            self.image.clip_draw(0,0,2048,512,self.x + self.dir * size_x / 2, self.y, size_x, size_y)
        else:
            self.image.clip_composite_draw(0,0,2048,512, 0, 'h', self.x + self.dir * size_x / 2, self.y, size_x, size_y)

        # draw_rectangle(*self.get_bb(), 0, 0, 255)

    def get_bb(self):
        size_x, size_y = self.width - self.count * self.d_width, self.height - self.count * self.d_height
        return (self.x, self.y - size_y / 4, self.x + self.dir * size_x, self.y + size_y / 4)

    def handle_collision(self, group, other):
        pass