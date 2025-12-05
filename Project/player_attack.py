from pico2d import draw_rectangle
import common

class PlayerAttack:
    def __init__(self, x = 0, y = 0, player = None):
        self.player = player
        self.x, self.y = x, y

    def update(self):
        self.x = self.player.x
        self.y = self.player.y

    def draw(self):
        # draw_rectangle(*self.get_bb(), 0, 255, 0)
        pass

    def get_bb(self):
        # face_dir에 따라 공격 범위 설정
        if self.player.face_dir == 1:  # 오른쪽을 보고 있을 때
            x_min = -0
            x_max = 100
        else:  # 왼쪽을 보고 있을 때
            x_min = -100
            x_max = 0

        if common.is_scrolling:
            sx = self.x - common.ground_1.window_left
            sy = self.y - common.ground_1.window_bottom
            return (sx + x_min, sy - 50, sx + x_max, sy + 100)
        else:
            return (self.x + x_min, self.y - 50, self.x + x_max, self.y + 100)

    def handle_collision(self, group, other):
        pass