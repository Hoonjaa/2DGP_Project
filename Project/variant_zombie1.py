from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
VZ1_SIZE_RATE = (250 / 120)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,541,61,66),(68,541,57,68),(130,541,59,65),(194,541,92,59),(291,541,60,45),
                       (356,541,60,43),(421,541,59,43),(485,541,60,47),(550,541,53,53),(608,541,40,58))

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


class Teleport_Out:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,756,52,64),(59,756,56,63),(120,756,56,57),(181,756,49,60))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Teleport_In:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,676,40,65),(47,676,44,67),(96,676,45,72),(146,676,45,68))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,915,45,61),(52,915,47,59),(104,915,49,57),(158,915,52,55),(215,915,53,54),
                       (273,915,54,54),(332,915,54,56),(391,915,52,58),(448,915,51,59),(504,915,48,60))

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


class VZ1:
    image = None
    def __init__(self):
        self.x, self.y = 700, 105
        self.hp = 250

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if VZ1.image is None:
            VZ1.image = load_image('Sprite/Variant Zombie1.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.TP_IN = Teleport_In(self)
        self.TP_OUT = Teleport_Out(self)
        self.ATTACK = Attack(self)
        self.state_machine = StateMachine(
            self.ATTACK,
            {
                self.IDLE: {},
                self.TP_IN: {},
                self.TP_OUT: {},
                self.ATTACK: {},
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

        max_height = 60  # 첫 프레임 높이
        current_height = action[self.frame][3]
        y_offset = self.y - (max_height - current_height) * VZ1_SIZE_RATE / 2
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, y_offset,
                                 action[self.frame][2] * VZ1_SIZE_RATE,
                                 action[self.frame][3] * VZ1_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, y_offset,
                                           action[self.frame][2] * VZ1_SIZE_RATE,
                                           action[self.frame][3] * VZ1_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * VZ1_SIZE_RATE / 2
        y_offset = action[self.frame][3] * VZ1_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 61
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * VZ1_SIZE_RATE / 2

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