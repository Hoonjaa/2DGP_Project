from pico2d import load_image

player_sprite = ( #0: IDLE, 1: WALK, 2: DASH, 3: JUMP
    ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48)),
    ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43)),
    ((7, 1720, 54, 35), (70, 1720, 74, 37), (153, 1720, 63, 35), (225, 1720, 57, 35), (291, 1720, 56, 35), (356, 1720, 55, 35), (420, 1720, 54, 35)),
    ((7, 1655, 43, 47), (59, 1655, 43, 47), (111, 1655, 43, 47)),
)

class Player:
    def __init__(self):
        self.x, self.y = 640, 90
        self.face_dir = 1
        self.dir = 0

        self.action = player_sprite[0]
        self.frame = 0
        self.image = load_image('Sprite/Player.png')

    def update(self):
        self.frame = (self.frame + 1) % len(self.action)

    def draw(self):
        self.image.clip_draw(*self.action[self.frame], self.x, self.y, 100, 100)