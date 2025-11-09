from pico2d import load_image
import game_world
import game_framework

from state_machine import StateMachine

PIXEL_PER_METER = (1.0 / 0.02) # 1 pixel 2 cm
# 중력 처리
GRAVITY_MPS2 = 9.8
GRAVITY_PPS2 = GRAVITY_MPS2 * PIXEL_PER_METER
# 애니메이션 속도 계산
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 좀비 크기 비율
ZOMBIE_SIZE_RATE = (200 / 120)

class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,420,43,61),(53,420,44,60),(103,420,45,59),(154,420,46,59),(206,420,45,60),(257,420,44,61))

    def enter(self, e):
        self.monster.dir = 0
        self.monster.frame = 0
        self.monster.anim_progress = 0.0

    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Zombie:
    image = None
    def __init__(self):
        self.x, self.y = 740, 90

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Zombie.image is None:
            Zombie.image = load_image('Sprite/Zombie.png')

        # 낙하 관련 변수
        self.ground_y = self.y
        self.dropSpeed = 8.0 * PIXEL_PER_METER

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
                # self.RUN: {},
                # self.JUMP: {},
                # self.HIT: {},
                # self.DIE: {},
                # self.ATTACK: {},
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
            self.image.clip_draw(*rect, self.x, self.y, action[self.frame][2] * ZOMBIE_SIZE_RATE, action[self.frame][3] * ZOMBIE_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, self.y, action[self.frame][2] * ZOMBIE_SIZE_RATE, action[self.frame][3] * ZOMBIE_SIZE_RATE)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        self.state_machine.get_bb()