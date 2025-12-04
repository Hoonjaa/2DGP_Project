import math
from pico2d import *
import game_framework
import common

class MonsterUI:
    def __init__(self, monster):
        self.x, self.y = monster.x - 40, monster.y + monster.monster_ui_offset_y
        self.monster = monster
        self.prev_hp = monster.hp  # 이전 프레임의 체력
        self.shake_time = 0  # 흔들림 남은 시간
        self.shake_duration = 0.3  # 흔들림 지속 시간
        self.shake_intensity = 4  # 흔들림 강도

    def update(self):
        self.x, self.y = self.monster.x - 40, self.monster.y + self.monster.monster_ui_offset_y

        # 체력이 감소했는지 확인
        if self.monster.hp < self.prev_hp:
            self.shake_time = self.shake_duration  # 흔들림 시작

        self.prev_hp = self.monster.hp

        # 흔들림 시간 감소
        if self.shake_time > 0:
            self.shake_time -= game_framework.frame_time
            if self.shake_time < 0:
                self.shake_time = 0

    def draw(self):
        # 흔들림 오프셋 계산
        shake_x = 0
        shake_y = 0
        if self.shake_time > 0:
            # sin 함수로 진동 효과 (빠른 진동)
            shake_x = math.sin(self.shake_time * 50) * self.shake_intensity
            shake_y = math.cos(self.shake_time * 40) * self.shake_intensity * 0.5

        # 스크롤링 적용된 화면 좌표 계산
        screen_x = self.x - common.ground_1.window_left + shake_x
        screen_y = self.y - common.ground_1.window_bottom + shake_y

        # Draw health bar
        health_bar_width = 80
        health_bar_height = 7
        health_percentage = max(0, min(1, self.monster.hp / self.monster.max_hp))
        filled_width = int(health_bar_width * health_percentage)
        border_thickness = 2

        # Draw black border (outer rectangle)
        draw_rectangle(
            screen_x - border_thickness,
            screen_y - border_thickness,
            screen_x + health_bar_width + border_thickness,
            screen_y + health_bar_height + border_thickness,
            100, 100, 100, 0, True
        )

        # Draw background of health bar (red)
        draw_rectangle(screen_x, screen_y, screen_x + health_bar_width, screen_y + health_bar_height, 255, 0, 0, 0, True)
        # Draw filled part of health bar (green)
        draw_rectangle(screen_x, screen_y, screen_x + filled_width, screen_y + health_bar_height, 0, 255, 0, 0, True)
