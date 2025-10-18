from pico2d import load_image

from state_machine import StateMachine

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
        self.state_machine = StateMachine(self.IDLE)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()