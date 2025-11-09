from pico2d import load_image, draw_rectangle
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.02) # 1 pixel 2 cm
SLASH_SPEED_KMPH = 150.0 # Km / Hour
SLASH_SPEED_MPM = (SLASH_SPEED_KMPH * 1000.0 / 60.0)
SLASH_SPEED_MPS = (SLASH_SPEED_MPM / 60.0)
SLASH_SPEED_PPS = (SLASH_SPEED_MPS * PIXEL_PER_METER)

SLASH_SIZE_RATE = (300 / 128)  # 2.34375
SLASH_SRC_SIZE = 64
SLASH_DRAW_SIZE = SLASH_SRC_SIZE * 300 // 128  # == 150, int로 고정

class SlashEffect:
    image = None
    def __init__(self, x = 0, y = 0, dir = 0, player = None):
        self.player = player
        if SlashEffect.image is None:
            SlashEffect.image = load_image('Sprite/Player_skill_effect.png')
        self.x, self.y = x, y
        self.dir = dir
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 2
        self.x = self.x + self.dir * SLASH_SPEED_PPS * game_framework.frame_time
        if self.x < -64 or self.x > 1280 + 64:
            game_world.remove_object(self)

    def draw(self):
        dw = SLASH_DRAW_SIZE
        if self.dir == 1:
            self.image.clip_draw(self.frame * SLASH_SRC_SIZE, 0, SLASH_SRC_SIZE, SLASH_SRC_SIZE,
                                 self.x, self.y, dw, dw)
        else:
            self.image.clip_composite_draw(self.frame * SLASH_SRC_SIZE, 0, SLASH_SRC_SIZE, SLASH_SRC_SIZE,
                                           0, 'h', self.x, self.y, dw, dw)
        draw_rectangle(*self.get_bb(), 0, 255, 0)

    def get_bb(self):
        return (self.x - 50, self.y - 80, self.x + 50, self.y + 80)

    def handle_collision(self, group, other):
        pass