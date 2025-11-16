from pico2d import load_image, draw_rectangle
import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
BOSS_SIZE_RATE = (300 / 160)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1959,70,79),(86,1959,73,79),(168,1959,75,79),(252,1959,77,79),(338,1959,79,79),(426,1959,74,79))

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
        return (self.monster.x - 35 * BOSS_SIZE_RATE, self.monster.y - 20 * BOSS_SIZE_RATE,
                self.monster.x + 18 * BOSS_SIZE_RATE, self.monster.y + 40 * BOSS_SIZE_RATE)


class Boss:
    image = None

    def __init__(self):
        self.x, self.y = 300, 90
        self.hp = 250

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Boss.image is None:
            Boss.image = load_image('Sprite/Reaper.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
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
        y_offset = self.y - (max_height - current_height) * BOSS_SIZE_RATE / 2
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, y_offset,
                                 action[self.frame][2] * BOSS_SIZE_RATE,
                                 action[self.frame][3] * BOSS_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, y_offset,
                                           action[self.frame][2] * BOSS_SIZE_RATE,
                                           action[self.frame][3] * BOSS_SIZE_RATE)


    def get_bb(self):
        return self.state_machine.get_bb()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()