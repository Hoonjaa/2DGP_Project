from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP

from state_machine import StateMachine

# 이벤트 체크 함수
def a_down(e):
    return e[0] == 'INPUT' and e[1] == SDL_KEYDOWN and e[1] == 97

def a_up(e):
    return e[0] == 'INPUT' and e[1] == SDL_KEYUP and e[1] == 97

def d_down(e):
    return e[0] == 'INPUT' and e[1] == SDL_KEYDOWN and e[1] == 100

def d_up(e):
    return e[0] == 'INPUT' and e[1] == SDL_KEYUP and e[1] == 100


class Run:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43))

    def enter(self):
        self.player.dir = 1

    def exit(self):
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
            self.player.image.clip_composite_draw(*self.action[self.player.frame], 0, '', self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48))

    def enter(self):
        self.player.dir = 0

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % len(self.action)

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*self.action[self.player.frame], self.player.x, self.player.y, 100, 100)
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(*self.action[self.player.frame], 0, '', self.player.x, self.player.y, 100, 100)


class Player:
    def __init__(self):
        self.x, self.y = 640, 90
        self.face_dir = 1
        self.dir = 0

        self.frame = 0
        self.image = load_image('Sprite/Player.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.RUN,
            {
                self.IDLE : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN},
                self.RUN : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()