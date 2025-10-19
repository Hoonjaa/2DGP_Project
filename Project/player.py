from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE

from state_machine import StateMachine

# 이벤트 체크 함수
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == 97

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == 97

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == 100

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == 100

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def land(e):
    return e[0] == 'LAND'

def move_land(e):
    return e[0] == 'MOVE_LAND'

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
        self.player.frame = (self.player.frame + 1) % len(self.action)
        self.player.x += self.player.dir * 5
        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > 1280:
            self.player.x = 1280

        self.player.y += self.dropSpeed * 5
        self.dropSpeed -= 0.1
        if self.player.y < self.ground_y:
            self.player.y = self.ground_y
            self.dropSpeed = 3.0
            if self.player.dir == 0 : self.player.state_machine.handle_event(('LAND', None))
            else : self.player.state_machine.handle_event(('MOVE_LAND', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*self.action[self.player.frame], self.player.x, self.player.y, 100, 100)
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(*self.action[self.player.frame], 0, 'h', self.player.x, self.player.y, 100, 100)


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
        self.player.frame = (self.player.frame + 1) % len(self.action)
        self.player.x += self.player.dir * 5
        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > 1280:
            self.player.x = 1280

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*self.action[self.player.frame], self.player.x, self.player.y, 100, 100)
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(*self.action[self.player.frame], 0, 'h', self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48))

    def enter(self, e):
        self.player.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % len(self.action)

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*self.action[self.player.frame], self.player.x, self.player.y, 100, 100)
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(*self.action[self.player.frame], 0, 'h', self.player.x, self.player.y, 100, 100)


class Player:
    def __init__(self):
        self.x, self.y = 640, 90
        self.face_dir = 1
        self.dir = 0

        self.frame = 0
        self.image = load_image('Sprite/Player.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN, space_down : self.JUMP},
                self.RUN : {a_down : self.IDLE, d_down : self.IDLE, a_up : self.IDLE, d_up : self.IDLE, space_down : self.JUMP},
                self.JUMP : {a_down : self.JUMP, d_down : self.JUMP, a_up : self.JUMP, d_up : self.JUMP, land : self.IDLE, move_land : self.RUN},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()