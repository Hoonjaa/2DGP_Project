from pico2d import load_image

from state_machine import StateMachine

player_sprite = ( #0: IDLE, 1: WALK, 2: DASH, 3: JUMP
    ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48)),
    ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43)),
    ((7, 1720, 54, 35), (70, 1720, 74, 37), (153, 1720, 63, 35), (225, 1720, 57, 35), (291, 1720, 56, 35), (356, 1720, 55, 35), (420, 1720, 54, 35)),
    ((7, 1655, 43, 47), (59, 1655, 43, 47), (111, 1655, 43, 47)),
)

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self):
        self.player.dir = 0

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % len(self.player.action)

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*self.player.action[self.player.frame], self.player.x, self.player.y, 100, 100)
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(*self.player.action[self.player.frame], 0, '', self.player.x, self.player.y, 100, 100)

class Player:
    def __init__(self):
        self.x, self.y = 640, 90
        self.face_dir = 1
        self.dir = 0

        self.action = player_sprite[0]
        self.frame = 0
        self.image = load_image('Sprite/Player.png')

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(self.IDLE)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()