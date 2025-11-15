from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine


PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
BRUTE_SIZE_RATE = (400 / 120)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Death:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,9,69,78),(78,9,66,76),(150,9,65,54),(221,9,60,50),(287,9,87,36),
                       (380,9,86,25),(472,9,88,25),(566,9,88,25),(660,9,88,25),(754,9,88,25),
                       (848,9,88,25),(942,9,88,25),(1036,9,88,25))

    def enter(self, e):
        self.monster.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Hit:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,98,75,62),(3,98,75,62),(3,98,75,62),(3,98,75,62))

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


class Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,169,72,80),(81,169,73,80),(160,169,112,80),(278,169,90,80),(374,169,89,80),
                       (469,169,87,80),(562,169,76,80),(644,169,72,80),(722,169,61,80))

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


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,255,73,63),(81,255,78,63),(166,255,73,62),(247,255,68,63))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.5 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,325,67,62),(76,325,65,62),(147,325,67,62),(220,325,69,60),(295,325,71,60),
                       (372,325,71,60),(449,325,71,60),(526,325,70,61))

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


class Brute:
    image = None
    def __init__(self):
        self.x, self.y = 940, 165
        self.hp = 300

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Brute.image is None:
            Brute.image = load_image('Sprite/Brute.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Attack(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.DEATH,
            {
                self.IDLE: {},
                self.RUN: {},
                self.ATTACK: {},
                self.HIT: {},
                self.DEATH: {},
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

        max_height = 80  # 첫 프레임 높이
        current_height = action[self.frame][3]
        y_offset = self.y - (max_height - current_height) * BRUTE_SIZE_RATE / 2
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, y_offset,
                                         action[self.frame][2] * BRUTE_SIZE_RATE,
                                         action[self.frame][3] * BRUTE_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, y_offset,
                                                   action[self.frame][2] * BRUTE_SIZE_RATE,
                                                   action[self.frame][3] * BRUTE_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * BRUTE_SIZE_RATE / 2
        y_offset = action[self.frame][3] * BRUTE_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 80  # Idle 상태의 기준 높이
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * BRUTE_SIZE_RATE / 2

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

    def handle_collision(self, group, other):
        pass