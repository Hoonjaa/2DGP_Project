import math
from pico2d import *
from player import Player
import game_framework


class UltUI:
    def __init__(self, player):
        self.x, self.y = 60, 500
        self.player = player
        self.image = load_image('Sprite/keytile.png')

    def update(self):
        pass

    def draw(self):
        if self.player.ult_cooldown > 0:
            self.image.clip_draw(443, 207, 13, 14, self.x, self.y, 39, 42)
        else:
            self.image.clip_draw(443, 343, 13, 14, self.x, self.y, 39, 42)


class SlashUI:
    def __init__(self, player):
        self.x, self.y = 60, 550
        self.player = player
        self.image = load_image('Sprite/keytile.png')

    def update(self):
        pass

    def draw(self):
        if self.player.slash_cooldown > 0:
            self.image.clip_draw(426, 207, 13, 14, self.x, self.y, 39, 42)
        else:
            self.image.clip_draw(426, 343, 13, 14, self.x, self.y, 39, 42)


class ShiftUI:
    def __init__(self, player):
        self.x, self.y = 85, 600
        self.player = player
        self.image = load_image('Sprite/shift_key.png')

    def update(self):
        pass

    def draw(self):
        if self.player.dash_cooldown > 0:
            self.image.clip_draw(18, 10, 30, 14, self.x, self.y, 90, 42)
        else:
            self.image.clip_draw(18, 32, 30, 14, self.x, self.y, 90, 42)


class PlayerUI:
    def __init__(self, player):
        self.x, self.y = 50, 650
        self.player = player
        self.prev_hp = player.hp  # 이전 프레임의 체력
        self.shake_time = 0  # 흔들림 남은 시간
        self.shake_duration = 0.3  # 흔들림 지속 시간
        self.shake_intensity = 10  # 흔들림 강도

        # 키보드 UI 추가
        self.shift_ui = ShiftUI(player)
        self.slash_ui = SlashUI(player)
        self.ult_ui = UltUI(player)

    def update(self):
        # 체력이 감소했는지 확인
        if self.player.hp < self.prev_hp:
            self.shake_time = self.shake_duration  # 흔들림 시작

        self.prev_hp = self.player.hp

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

        # 흔들림 적용된 위치
        draw_x = self.x + shake_x
        draw_y = self.y + shake_y

        # Draw health bar
        health_bar_width = 300
        health_bar_height = 20
        health_percentage = self.player.hp / self.player.max_hp
        filled_width = int(health_bar_width * health_percentage)
        border_thickness = 3

        # Draw black border (outer rectangle)
        draw_rectangle(
            draw_x - border_thickness,
            draw_y - border_thickness,
            draw_x + health_bar_width + border_thickness,
            draw_y + health_bar_height + border_thickness,
            100, 100, 100, 0, True
        )

        # Draw background of health bar (red)
        draw_rectangle(draw_x, draw_y, draw_x + health_bar_width, draw_y + health_bar_height, 255, 0, 0, 0, True)
        # Draw filled part of health bar (green)
        draw_rectangle(draw_x, draw_y, draw_x + filled_width, draw_y + health_bar_height, 0, 255, 0, 0, True)

        # Draw shift UI
        self.shift_ui.draw()
        # Draw slash UI
        self.slash_ui.draw()
        # Draw ult UI
        self.ult_ui.draw()