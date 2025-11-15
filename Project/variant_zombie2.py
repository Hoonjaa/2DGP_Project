from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
VZ2_SIZE_RATE = (300 / 120)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,289,26,58),(36,289,27,57),(69,289,20,58),(95,289,18,59),(119,289,23,58),
                       (148,289,26,57),(180,289,26,58),(212,289,26,59))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,356,29,58),(39,356,29,57),(74,356,29,57),(109,356,28,57),(143,356,28,57),
                       (177,356,28,58),(211,356,28,58),(245,356,29,58))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class VZ2:
    image = None
    def __init__(self):
        self.x, self.y = 600, 115
        self.hp = 250

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if VZ2.image is None:
            VZ2.image = load_image('Sprite/Variant Zombie2.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.RUN,
            {
                self.IDLE: {},
                self.RUN: {},
            }
        )

    def next_frame(self, action):
        # 진행 누적
        self.anim_progress += ACTION_PER_TIME * game_framework.frame_time * len(action)
        # 정수 프레임 산출
        self.frame = int(self.anim_progress) % len(action)

    def draw_current(self, action):
        idx = self.frame % len(action)
        rect = action[idx]
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, self.y, action[self.frame][2] * VZ2_SIZE_RATE, action[self.frame][3] * VZ2_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * VZ2_SIZE_RATE / 2
        y_offset = action[self.frame][3] * VZ2_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 58  # Idle 상태의 기준 높이
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * VZ2_SIZE_RATE / 2

        return (self.x - x_offset, adjusted_y - y_offset,
              self.x + x_offset, adjusted_y + y_offset)

    def get_bb(self):
        return self.state_machine.get_bb()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()