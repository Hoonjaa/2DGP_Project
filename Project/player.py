from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_LSHIFT, SDLK_j

from state_machine import StateMachine

# 이벤트 체크 함수
def key_event(e, ev_type, key):
    return e[0] == 'INPUT' and e[1].type == ev_type and e[1].key == key

def a_down(e): return key_event(e, SDL_KEYDOWN, SDLK_a)
def a_up(e):   return key_event(e, SDL_KEYUP,   SDLK_a)
def d_down(e): return key_event(e, SDL_KEYDOWN, SDLK_d)
def d_up(e):   return key_event(e, SDL_KEYUP,   SDLK_d)
def space_down(e): return key_event(e, SDL_KEYDOWN, SDLK_SPACE)
def shift_down(e): return key_event(e, SDL_KEYDOWN, SDLK_LSHIFT)
def j_down(e): return key_event(e, SDL_KEYDOWN, SDLK_j)

def land(e): return e[0] == 'LAND'
def move_land(e): return e[0] == 'MOVE_LAND'
def dash_finish(e): return e[0] == 'DASH_FINISH'
def move_dash_finish(e): return e[0] == 'MOVE_DASH_FINISH'
def jump_dash_finish(e): return e[0] == 'JUMP_DASH_FINISH'
def attack_finish(e): return e[0] == 'ATTACK_FINISH'
def move_attack_finish(e): return e[0] == 'MOVE_ATTACK_FINISH'
def jump_attack_finish(e): return e[0] == 'JUMP_ATTACK_FINISH'





class Attack:
    def __init__(self, player):
        self.player = player
        self.action = ((7,1395,47,43),(63,1397,47,41),(119,1368,74,70),(202,1368,76,70),(287,1368,77,71),
                       (373,1381,97,57),(479,1360,101,78),(589,1370,95,68),(693,1371,90,67),(792,1368,97,70),
                       (898,1368,97,70),(1004,1365,79,73),(1092,1360,90,78),(1191,1381,92,57),(1292,1395,49,43),(1350,1396,48,42))
        self.large_frames = set(range(2, 14))
        self.base_size = 100
        self.large_size = 170

    def enter(self, e):
        self.player.frame = 0


    def exit(self, e):
        pass

    def do(self):
        if self.player.frame == len(self.action) - 1:
            if self.player.y > self.player.ground_y:
                event = 'JUMP_ATTACK_FINISH'
                self.player.dropSpeed = 0.0
            else:
                move_pressed = self.player.left_pressed or self.player.right_pressed
                event = 'MOVE_ATTACK_FINISH' if move_pressed else 'ATTACK_FINISH'
            self.player.state_machine.handle_event((event, None))

        self.player.next_frame(self.action)

    def draw(self):
        frame = self.player.frame
        size = self.large_size if frame in self.large_frames else self.base_size
        # 큰 프레임에서 발(바닥) 고정: 중심이 올라가는 만큼 내려줌
        y_render = self.player.y + 20 if frame in self.large_frames else self.player.y

        rect = self.action[frame]
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*rect, self.player.x, y_render, size, size)
        else:
            self.player.image.clip_composite_draw(*rect, 0, 'h', self.player.x, y_render, size, size)


class Dash:
    def __init__(self, player):
        self.player = player
        self.action = ((54,1722,54,35),(70,1720,74,37),(153,1722,63,35),(225,1722,57,35),(291,1722,56,35),(356,1722,55,35),(420,1722,54,35))

    def enter(self, e):
        self.player.frame = 0
        self.dash_dir = self.player.face_dir
        #추후에 플레이어 무적 상태 추가
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.player.frame == len(self.action) - 1:
            if self.player.y > self.player.ground_y:
                event = 'JUMP_DASH_FINISH'
                self.player.dropSpeed = 0.0
            else:
                move_pressed = self.player.left_pressed or self.player.right_pressed
                event = 'MOVE_DASH_FINISH' if move_pressed else 'DASH_FINISH'
            self.player.state_machine.handle_event((event, None))
        self.player.next_frame(self.action)
        self.player.x = max(0, min(1280, self.player.x + self.dash_dir * 20))


    def draw(self):
        self.player.draw_current(self.action)


class Jump:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1655, 43, 47), (59, 1655, 43, 47), (111, 1655, 43, 47))

    def enter(self, e):
        left = self.player.left_pressed
        right = self.player.right_pressed
        self.player.dir = (1 if right else 0) + (-1 if left else 0)
        if self.player.dir != 0:
            self.player.face_dir = 1 if self.player.dir > 0 else -1

    def exit(self, e):
        pass

    def do(self):
        self.player.next_frame(self.action)
        self.player.move_x()

        self.player.y += self.player.dropSpeed * 5
        self.player.dropSpeed -= 0.1
        if self.player.y < self.player.ground_y:
            self.player.y = self.player.ground_y
            self.player.dropSpeed = 3.0
            if self.player.dir == 0 : self.player.state_machine.handle_event(('LAND', None))
            else : self.player.state_machine.handle_event(('MOVE_LAND', None))

    def draw(self):
        self.player.draw_current(self.action)

class Run:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43))

    def enter(self, e):
        left = self.player.left_pressed
        right = self.player.right_pressed
        self.player.dir = (1 if right else 0) + (-1 if left else 0)
        if self.player.dir != 0:
            self.player.face_dir = 1 if self.player.dir > 0 else -1

    def exit(self, e):
        pass

    def do(self):
        self.player.next_frame(self.action)
        self.player.move_x()

    def draw(self):
        self.player.draw_current(self.action)


class Idle:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48))

    def enter(self, e):
        self.player.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.next_frame(self.action)

    def draw(self):
        self.player.draw_current(self.action)

class Player:
    def __init__(self):
        self.x, self.y = 640, 90

        # 점프 관련 변수
        self.ground_y = self.y
        self.dropSpeed = 3.0

        # 방향 변수
        self.face_dir = 1
        self.dir = 0
        self.left_pressed = False
        self.right_pressed = False

        # 애니메이션 변수
        self.frame = 0
        self.image = load_image('Sprite/Player.png')

        # 상태머신
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DASH = Dash(self)
        self.ATTACK = Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN, space_down : self.JUMP, shift_down : self.DASH, j_down : self.ATTACK},
                self.RUN : {a_down : self.IDLE, d_down : self.IDLE, a_up : self.IDLE, d_up : self.IDLE, space_down : self.JUMP, shift_down : self.DASH, j_down : self.ATTACK},
                self.JUMP : {a_down : self.JUMP, d_down : self.JUMP, a_up : self.JUMP, d_up : self.JUMP, land : self.IDLE, move_land : self.RUN, shift_down : self.DASH, j_down : self.ATTACK},
                self.DASH : {dash_finish : self.IDLE, move_dash_finish : self.RUN, jump_dash_finish : self.JUMP},
                self.ATTACK : {attack_finish : self.IDLE, move_attack_finish : self.RUN, jump_attack_finish : self.JUMP},
            }
        )

    def next_frame(self, action):
        self.frame = (self.frame + 1) % len(action)

    def move_x(self):
        self.x = max(0, min(1280, self.x + self.dir * 5))

    def draw_current(self, action):
        rect = action[self.frame]
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, self.y, 100, 100)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 전역 키 눌림 상태 갱신
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.left_pressed = True
            elif event.key == SDLK_d:
                self.right_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.left_pressed = False
            elif event.key == SDLK_d:
                self.right_pressed = False
        # 눌림 상태로 항상 최신 dir 계산
        self.dir = (1 if self.right_pressed else 0) + (-1 if self.left_pressed else 0)
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()