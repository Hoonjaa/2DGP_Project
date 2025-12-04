from pico2d import load_font
import game_world
import game_framework
import common

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
        # 스크롤링 적용된 화면 좌표 계산
        screen_x = self.x - common.ground_1.window_left
        screen_y = self.y - common.ground_1.window_bottom
        DamageText.font.draw(screen_x, screen_y, str(self.damage), (255, 0, 0))
