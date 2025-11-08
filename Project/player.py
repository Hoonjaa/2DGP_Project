from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_LSHIFT

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

def land(e): return e[0] == 'LAND'
def move_land(e): return e[0] == 'MOVE_LAND'
def dash_finish(e): return e[0] == 'DASH_FINISH'
def move_dash_finish(e): return e[0] == 'MOVE_DASH_FINISH'


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
            event = 'MOVE_DASH_FINISH' if self.player.dir != 0 else 'DASH_FINISH'
            self.player.state_machine.handle_event((event, None))
        self.player.next_frame(self.action)
        self.player.x = max(0, min(1280, self.player.x + self.dash_dir * 20))


    def draw(self):
        self.player.draw_current(self.action)


class Jump:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1655, 43, 47), (59, 1655, 43, 47), (111, 1655, 43, 47))
        self.dropSpeed = 3.0
        self.ground_y = player.y

    def enter(self, e):
        if a_down(e) or d_up(e):
            if self.player.dir == 1 : self.player.dir = 0
            else : self.player.dir = -1
            if self.player.dir == 0 : self.player.face_dir = 1
            else : self.player.face_dir = -1
        elif d_down(e) or a_up(e):
            if self.player.dir == -1 : self.player.dir = 0
            else : self.player.dir = 1
            if self.player.dir == 0 : self.player.face_dir = -1
            else : self.player.face_dir = 1

    def exit(self, e):
        pass

    def do(self):
        self.player.next_frame(self.action)
        self.player.move_x()

        self.player.y += self.dropSpeed * 5
        self.dropSpeed -= 0.1
        if self.player.y < self.ground_y:
            self.player.y = self.ground_y
            self.dropSpeed = 3.0
            if self.player.dir == 0 : self.player.state_machine.handle_event(('LAND', None))
            else : self.player.state_machine.handle_event(('MOVE_LAND', None))

    def draw(self):
        self.player.draw_current(self.action)

class Run:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43))

    def enter(self, e):
        if a_down(e) or d_up(e):
            self.player.dir = -1
            self.player.face_dir = -1
        elif d_down(e) or a_up(e):
            self.player.dir = 1
            self.player.face_dir = 1

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


        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 애니메이션 변수
        self.frame = 0
        self.image = load_image('Sprite/Player.png')

        # 상태머신
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DASH = Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN, space_down : self.JUMP, shift_down : self.DASH},
                self.RUN : {a_down : self.IDLE, d_down : self.IDLE, a_up : self.IDLE, d_up : self.IDLE, space_down : self.JUMP, shift_down : self.DASH},
                self.JUMP : {a_down : self.JUMP, d_down : self.JUMP, a_up : self.JUMP, d_up : self.JUMP, land : self.IDLE, move_land : self.RUN},
                self.DASH : {dash_finish : self.IDLE, move_dash_finish : self.RUN},
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
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()