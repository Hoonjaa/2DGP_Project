from pico2d import *
import common
import game_world
import game_framework

class Jewel:
    def __init__(self, x = 0, y = 0, price = 0):
        self.x, self.y = x, 60
        self.price = price
        self.image = load_image('Sprite/jewel.png')
        self.sound = load_wav('Sound/coin.mp3')
        self.is_flying = False
        self.start_x = 0
        self.start_y = 0
        self.target_x = 1100
        self.target_y = 650
        self.fly_progress = 0.0
        self.fly_speed = 2.0  # 초당 진행도 (0~1)

    def update(self):
        if self.is_flying:
            # 프레임 시간 기반으로 진행도 증가
            self.fly_progress += self.fly_speed * game_framework.frame_time

            if self.fly_progress >= 1.0:
                # 목적지 도착
                common.player.jewel += self.price
                game_world.remove_object(self)
            else:
                # 베지어 곡선으로 이동 (2차 베지어 곡선)
                t = self.fly_progress

                # 제어점 계산 (시작점과 끝점 사이의 위쪽에 위치)
                control_x = (self.start_x + self.target_x) / 2
                control_y = max(self.start_y, self.target_y) + 200

                # 베지어 곡선 공식: B(t) = (1-t)^2*P0 + 2*(1-t)*t*P1 + t^2*P2
                self.x = (1-t)**2 * self.start_x + 2*(1-t)*t * control_x + t**2 * self.target_x
                self.y = (1-t)**2 * self.start_y + 2*(1-t)*t * control_y + t**2 * self.target_y

    def draw(self):
        if self.is_flying:
            # 날아가는 중에는 화면 좌표 그대로 사용
            self.image.clip_draw(0, 0, 80, 80, self.x, self.y, 40, 40)
        else:
            # 일반 상태에서는 월드 좌표 변환
            sx = self.x - common.ground_1.window_left
            sy = self.y - common.ground_1.window_bottom
            self.image.clip_draw(0, 0, 80, 80, sx, sy, 40, 40)

        if not self.is_flying:
            draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        if self.is_flying:
            return (0, 0, 0, 0)  # 날아가는 중에는 충돌 무시
        screen_x = self.x - common.ground_1.window_left
        screen_y = self.y - common.ground_1.window_bottom
        return (screen_x - 20, screen_y - 20, screen_x + 20, screen_y + 20)

    def handle_collision(self, group, other):
        if group == 'player:jewel' and not self.is_flying:
            # 날아가기 시작
            self.sound.set_volume(32)
            self.sound.play()
            self.is_flying = True
            self.start_x = self.x - common.ground_1.window_left
            self.start_y = self.y - common.ground_1.window_bottom
            self.x = self.start_x
            self.y = self.start_y
            self.fly_progress = 0.0
