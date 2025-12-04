from pico2d import *
import common

class ScrollRedSky:
    def __init__(self):
        self.image = load_image('Sprite/sky2.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.tile_w = self.image.w
        self.w = 7680
        self.h = self.image.h

        # 초기 윈도우 위치 설정
        self.window_left = 0
        self.window_bottom = 0

    def update(self):
        self.window_left = clamp(0, int(common.player.x // 2), self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y // 2), self.h - self.ch - 1)
        # self.window_left = clamp(0, int(common.player.x // 2) - self.cw // 2, self.w - self.cw - 1)
        # self.window_bottom = clamp(0, int(common.player.y // 2) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        start_tile = self.window_left // self.tile_w
        num_tiles = (self.cw // self.tile_w) + 2
        for i in range(num_tiles):
            tile_idx = start_tile + i
            if tile_idx * self.tile_w >= self.w:
                break

            # 타일의 월드 좌표
            tile_world_x = tile_idx * self.tile_w
            # 화면 좌표로 변환
            tile_screen_x = tile_world_x - self.window_left

            if tile_idx % 2 == 0:
                self.image.clip_draw_to_origin(0, self.window_bottom, self.tile_w, self.ch, tile_screen_x, 0)
            else: # 반전된 이미지 그리기
                self.image.clip_composite_draw(0, self.window_bottom, self.tile_w, self.ch, 0, 'h', tile_screen_x + self.tile_w // 2, self.ch // 2, self.tile_w, self.ch)