from pico2d import *
import common
import game_world
import game_framework
from slash_effect import SlashEffect
from player_attack import PlayerAttack
from player_ult_attack import PlayerUltAttack
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_LSHIFT, SDLK_j, SDLK_k, SDLK_l

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
def k_down(e): return key_event(e, SDL_KEYDOWN, SDLK_k)
def l_down(e): return key_event(e, SDL_KEYDOWN, SDLK_l)

def reset(e): return e[0] == 'RESET'
def land(e): return e[0] == 'LAND'
def move_land(e): return e[0] == 'MOVE_LAND'
def dash_finish(e): return e[0] == 'DASH_FINISH'
def move_dash_finish(e): return e[0] == 'MOVE_DASH_FINISH'
def jump_dash_finish(e): return e[0] == 'JUMP_DASH_FINISH'
def attack_finish(e): return e[0] == 'ATTACK_FINISH'
def move_attack_finish(e): return e[0] == 'MOVE_ATTACK_FINISH'
def jump_attack_finish(e): return e[0] == 'JUMP_ATTACK_FINISH'
def slash_finish(e): return e[0] == 'SLASH_FINISH'
def move_slash_finish(e): return e[0] == 'MOVE_SLASH_FINISH'
def jump_slash_finish(e): return e[0] == 'JUMP_SLASH_FINISH'
def ultimate_finish(e): return e[0] == 'ULTIMATE_FINISH'
def move_ultimate_finish(e): return e[0] == 'MOVE_ULTIMATE_FINISH'


# 플레이어 속도 계산
PIXEL_PER_METER = (1.0 / 0.02) # 1 pixel 2 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# 대쉬 속도 계산
DASH_SPEED_KMPH = 170.0 # Km / Hour
DASH_SPEED_MPM = (DASH_SPEED_KMPH * 1000.0 / 60.0)
DASH_SPEED_MPS = (DASH_SPEED_MPM / 60.0)
DASH_SPEED_PPS = (DASH_SPEED_MPS * PIXEL_PER_METER)
# 중력 처리
GRAVITY_MPS2 = 9.8
GRAVITY_PPS2 = GRAVITY_MPS2 * PIXEL_PER_METER
# 애니메이션 속도 계산
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 플레이어 크기 배율
PLAYER_SIZE_RATE = (200 / 96)


class Ultimate:
    def __init__(self, player):
        self.player = player
        self.action = ((7,306,160,43),(176,308,158,41),(343,276,164,73),(516,271,170,78),(695,292,184,57),
                       (888,271,194,78),(1091,281,188,68),(7,200,190,67),(206,197,192,70),(407,197,154,70),
                       (570,197,164,70),(743,196,164,71),(916,210,184,57),(1109,189,194,78),(7,117,188,68),
                       (204,118,190,67),(403,115,192,70),(604,115,196,70),(809,112,164,73),(982,107,170,78),
                       (1161,142,160,43),(7,60,160,43),(176,60,160,43),(343,60,160,43))
        self.ult_attack = None

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0

        self.player.ult_cooldown = self.player.ult_cooldown_time

        self.ult_attack = PlayerUltAttack(self.player.x, self.player.y, self.player)
        game_world.add_object(self.ult_attack, 2)
        game_world.add_collision_pair('monster:player_ult', None, self.ult_attack)

    def exit(self, e):
        game_world.remove_object(self.ult_attack)

    def do(self):
        if self.player.frame == len(self.action) - 1:
            move_pressed = self.player.left_pressed or self.player.right_pressed
            event = 'MOVE_ULTIMATE_FINISH' if move_pressed else 'ULTIMATE_FINISH'
            self.player.state_machine.handle_event((event, None))

        self.player.anim_progress += 0.8 * game_framework.frame_time * len(self.action)
        self.player.frame = int(self.player.anim_progress) % len(self.action)

    def draw(self):
        frame = self.player.frame
        size_x, size_y = self.action[self.player.frame][2] * PLAYER_SIZE_RATE, self.action[self.player.frame][3] * PLAYER_SIZE_RATE
        x_render = self.player.x + (self.action[self.player.frame][2] - 48) / 2 * PLAYER_SIZE_RATE * self.player.face_dir
        y_render = self.player.y + (self.action[self.player.frame][3] - 48) / 2 * PLAYER_SIZE_RATE

        # 스크롤링 지원
        if common.is_scrolling:
            sx = x_render - common.ground_1.window_left
            sy = y_render - common.ground_1.window_bottom
        else:
            sx = x_render
            sy = y_render

        rect = self.action[frame]
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*rect, sx, sy, size_x, size_y)
        else:
            self.player.image.clip_composite_draw(*rect, 0, 'h', sx, sy, size_x, size_y)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = 50 * PLAYER_SIZE_RATE / 2
        x_correct = 20 * PLAYER_SIZE_RATE * self.player.face_dir
        y_offset = 50 * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset + x_correct, sy - y_offset, sx + x_offset + x_correct, sy + y_offset)
        else:
            return (self.player.x - x_offset + x_correct, self.player.y - y_offset, self.player.x + x_offset + x_correct, self.player.y + y_offset)


class Slash:
    def __init__(self, player):
        self.player = player
        self.action = ((7,369,49,43),(65,370,48,42),(122,366,59,46),(190,372,47,40),(246,377,44,35))

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0
        self.player.slash_cooldown = self.player.slash_cooldown_time

    def exit(self, e):
        self.player.add_slash_effect()

    def do(self):
        if self.player.frame == len(self.action) - 1:
            if self.player.y > self.player.ground_y:
                event = 'JUMP_SLASH_FINISH'
                self.player.dropSpeed = 0.0
            else:
                move_pressed = self.player.left_pressed or self.player.right_pressed
                event = 'MOVE_SLASH_FINISH' if move_pressed else 'SLASH_FINISH'
            self.player.state_machine.handle_event((event, None))
        self.player.next_frame(self.action)

    def draw(self):
        self.player.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = self.action[self.player.frame][2] * PLAYER_SIZE_RATE / 2
        y_offset = self.action[self.player.frame][3] * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset, sy - y_offset, sx + x_offset, sy + y_offset)
        else:
            return (self.player.x - x_offset, self.player.y - y_offset, self.player.x + x_offset, self.player.y + y_offset)


class Attack:
    def __init__(self, player):
        self.player = player
        self.action = ((7,1395,47,43),(63,1397,47,41),(119,1368,74,70),(202,1368,76,70),(287,1368,77,71),
                       (373,1381,97,57),(479,1360,101,78),(589,1370,95,68),(693,1371,90,67),(792,1368,97,70),
                       (898,1368,97,70),(1004,1365,79,73),(1092,1360,90,78),(1191,1381,92,57),(1292,1395,49,43),(1350,1396,48,42))
        self.attack = None

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0

        self.attack = PlayerAttack(self.player.x, self.player.y, self.player)
        game_world.add_object(self.attack, 2)
        game_world.add_collision_pair('monster:player_attack', None, self.attack)


    def exit(self, e):
        game_world.remove_object(self.attack)

    def do(self):
        if self.player.frame == len(self.action) - 1:
            if self.player.y > self.player.ground_y:
                event = 'JUMP_ATTACK_FINISH'
                self.player.dropSpeed = 0.0
            else:
                move_pressed = self.player.left_pressed or self.player.right_pressed
                event = 'MOVE_ATTACK_FINISH' if move_pressed else 'ATTACK_FINISH'
            self.player.state_machine.handle_event((event, None))

        self.player.anim_progress += 1.5 * game_framework.frame_time * len(self.action)
        self.player.frame = int(self.player.anim_progress) % len(self.action)

    def draw(self):
        frame = self.player.frame
        size_x, size_y = self.action[self.player.frame][2] * PLAYER_SIZE_RATE, self.action[self.player.frame][3] * PLAYER_SIZE_RATE
        # 큰 프레임에서 발(바닥) 고정: 중심이 올라가는 만큼 내려줌
        y_render = self.player.y + (self.action[self.player.frame][3] - 48) / 2 * PLAYER_SIZE_RATE

        # 스크롤링 지원
        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = y_render - common.ground_1.window_bottom
        else:
            sx = self.player.x
            sy = y_render

        rect = self.action[frame]
        if self.player.face_dir == 1:
            self.player.image.clip_draw(*rect, sx, sy, size_x, size_y)
        else:
            self.player.image.clip_composite_draw(*rect, 0, 'h', sx, sy, size_x, size_y)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = 50 * PLAYER_SIZE_RATE / 2
        y_offset = 50 * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset, sy - y_offset, sx + x_offset, sy + y_offset)
        else:
            return (self.player.x - x_offset, self.player.y - y_offset, self.player.x + x_offset, self.player.y + y_offset)


class Dash:
    def __init__(self, player):
        self.player = player
        self.action = ((7,1722,54,35),(70,1720,74,37),(153,1722,63,35),(225,1722,57,35),(291,1722,56,35),(356,1722,55,35),(420,1722,54,35))

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0
        self.dash_dir = self.player.face_dir
        self.player.dash_cooldown = self.player.dash_cooldown_time
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

        # 대쉬 전용 프레임 진행
        self.player.anim_progress += 7.0 * game_framework.frame_time * len(self.action)
        self.player.frame = int(self.player.anim_progress) % len(self.action)

        # 스크롤링 여부에 따른 이동 범위 설정
        if common.is_scrolling:
            self.player.x = max(0, min(7680, self.player.x + self.dash_dir * DASH_SPEED_PPS * game_framework.frame_time))
        else:
            self.player.x = max(0, min(1280, self.player.x + self.dash_dir * DASH_SPEED_PPS * game_framework.frame_time))


    def draw(self):
        self.player.draw_current(self.action)

    def get_bb(self):
        pass


class Jump:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1655, 43, 47), (59, 1655, 43, 47), (111, 1655, 43, 47))

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0
        # 방향 설정
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

        # 중력 적용
        dt = game_framework.frame_time
        self.player.y += self.player.dropSpeed * dt
        self.player.dropSpeed -= GRAVITY_PPS2 * dt

        # 착지시 처리
        if self.player.y < self.player.ground_y:
            self.player.y = self.player.ground_y
            self.player.dropSpeed = 8.0 * PIXEL_PER_METER
            if self.player.dir == 0 : self.player.state_machine.handle_event(('LAND', None))
            else : self.player.state_machine.handle_event(('MOVE_LAND', None))

    def draw(self):
        self.player.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = self.action[self.player.frame][2] * PLAYER_SIZE_RATE / 2
        y_offset = self.action[self.player.frame][3] * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset, sy - y_offset, sx + x_offset, sy + y_offset)
        else:
            return (self.player.x - x_offset, self.player.y - y_offset, self.player.x + x_offset, self.player.y + y_offset)

class Run:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1777, 54, 41), (70, 1777, 53, 40), (132, 1777, 53, 41), (194, 1777, 53, 41), (256, 1777, 52, 40), (317, 1776, 52, 43))

    def enter(self, e):
        self.player.frame = 0
        self.player.anim_progress = 0.0
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
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = self.action[self.player.frame][2] * PLAYER_SIZE_RATE / 2
        y_offset = self.action[self.player.frame][3] * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset, sy - y_offset, sx + x_offset, sy + y_offset)
        else:
            return (self.player.x - x_offset, self.player.y - y_offset, self.player.x + x_offset, self.player.y + y_offset)


class Idle:
    def __init__(self, player):
        self.player = player
        self.action = ((7, 1835, 49, 46), (65, 1835, 49, 46), (123, 1835, 49, 47), (181, 1835, 49, 48), (239, 1835, 49, 48), (297, 1835, 49, 48), (355, 1835, 49, 48))

    def enter(self, e):
        self.player.dir = 0
        self.player.frame = 0
        self.player.anim_progress = 0.0

    def exit(self, e):
        pass

    def do(self):
        self.player.next_frame(self.action)

    def draw(self):
        self.player.draw_current(self.action)
        draw_rectangle(*self.get_bb(),255,0,0)

    def get_bb(self):
        x_offset = self.action[self.player.frame][2] * PLAYER_SIZE_RATE / 2
        y_offset = self.action[self.player.frame][3] * PLAYER_SIZE_RATE / 2

        if common.is_scrolling:
            sx = self.player.x - common.ground_1.window_left
            sy = self.player.y - common.ground_1.window_bottom
            return (sx - x_offset, sy - y_offset, sx + x_offset, sy + y_offset)
        else:
            return (self.player.x - x_offset, self.player.y - y_offset, self.player.x + x_offset, self.player.y + y_offset)

class Player:
    def __init__(self):
        self.x, self.y = 640, 85
        self.hp = 2
        self.max_hp = 300

        # 스킬 잠금 관련 변수
        self.is_slash_unlocked = True
        self.is_ult_unlocked = True

        # 재화 관련 변수
        self.jewel = 0

        #데미지 관련 변수
        self.base_damage = 10
        self.slash_damage = 30
        self.ult_damage = 30

        # 스킬 쿨타임 변수
        self.slash_cooldown = 0.0
        self.slash_cooldown_time = 3.0
        self.ult_cooldown = 0.0
        self.ult_cooldown_time = 10.0

        # 대쉬 쿨타임 변수
        self.dash_cooldown = 0.0
        self.dash_cooldown_time = 0.5

        # 점프 관련 변수
        self.ground_y = self.y
        self.dropSpeed = 8.0 * PIXEL_PER_METER

        # 방향 변수
        self.face_dir = 1
        self.dir = 0
        self.left_pressed = False
        self.right_pressed = False

        # 애니메이션 변수
        self.frame = 0
        self.anim_progress = 0.0
        self.image = load_image('Sprite/Player.png')

        #맞고 있는 중인지 판정 변수
        self.is_hit = False
        self.hit_timer = 0.0

        # 상태머신
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DASH = Dash(self)
        self.ATTACK = Attack(self)
        self.SLASH = Slash(self)
        self.ULTIMATE = Ultimate(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {a_down : self.RUN, d_down : self.RUN, a_up : self.RUN, d_up : self.RUN, space_down : self.JUMP, shift_down : self.DASH, j_down : self.ATTACK, k_down : self.SLASH, l_down : self.ULTIMATE},
                self.RUN : {a_down : self.IDLE, d_down : self.IDLE, a_up : self.IDLE, d_up : self.IDLE, space_down : self.JUMP, shift_down : self.DASH, j_down : self.ATTACK, k_down : self.SLASH, l_down : self.ULTIMATE, reset : self.IDLE},
                self.JUMP : {a_down : self.JUMP, d_down : self.JUMP, a_up : self.JUMP, d_up : self.JUMP, land : self.IDLE, move_land : self.RUN, shift_down : self.DASH, j_down : self.ATTACK, k_down : self.SLASH},
                self.DASH : {dash_finish : self.IDLE, move_dash_finish : self.RUN, jump_dash_finish : self.JUMP},
                self.ATTACK : {attack_finish : self.IDLE, move_attack_finish : self.RUN, jump_attack_finish : self.JUMP},
                self.SLASH : {slash_finish : self.IDLE, move_slash_finish : self.RUN, jump_slash_finish : self.JUMP},
                self.ULTIMATE : {ultimate_finish : self.IDLE, move_ultimate_finish : self.RUN},
            }
        )

    def next_frame(self, action):
        # 진행 누적
        self.anim_progress += ACTION_PER_TIME * game_framework.frame_time * len(action)
        # 정수 프레임 산출
        self.frame = int(self.anim_progress) % len(action)

    def move_x(self):
        if common.is_scrolling:
            self.x = max(20, min(7680, self.x + self.dir * RUN_SPEED_PPS * game_framework.frame_time))
        else:
            self.x = max(20, min(1280, self.x + self.dir * RUN_SPEED_PPS * game_framework.frame_time))

    def draw_current(self, action):
        idx = self.frame % len(action)
        rect = action[idx]

        if common.is_scrolling:
            sx = self.x - common.ground_1.window_left
            sy = self.y - common.ground_1.window_bottom
            if self.face_dir == 1:
                self.image.clip_draw(*rect, sx, sy, action[self.frame][2] * PLAYER_SIZE_RATE, action[self.frame][3] * PLAYER_SIZE_RATE)
            else:
                self.image.clip_composite_draw(*rect, 0, 'h', sx, sy, action[self.frame][2] * PLAYER_SIZE_RATE, action[self.frame][3] * PLAYER_SIZE_RATE)
        else:
            if self.face_dir == 1:
                self.image.clip_draw(*rect, self.x, self.y, action[self.frame][2] * PLAYER_SIZE_RATE, action[self.frame][3] * PLAYER_SIZE_RATE)
            else:
                self.image.clip_composite_draw(*rect, 0, 'h', self.x, self.y, action[self.frame][2] * PLAYER_SIZE_RATE, action[self.frame][3] * PLAYER_SIZE_RATE)

    def update(self):
        self.state_machine.update()

        if common.is_scrolling:
            self.x = clamp(20, self.x, common.ground_1.w - 10)
            self.y = clamp(20, self.y, common.ground_1.h - 10)

        if self.is_hit:
            self.hit_timer += game_framework.frame_time
            if self.hit_timer >= 1.0:
                self.is_hit = False
                self.hit_timer = 0.0

        # 쿨타임 감소
        if self.slash_cooldown > 0:
            self.slash_cooldown -= game_framework.frame_time
            if self.slash_cooldown < 0:
                self.slash_cooldown = 0

        if self.dash_cooldown > 0:
            self.dash_cooldown -= game_framework.frame_time
            if self.dash_cooldown < 0:
                self.dash_cooldown = 0

        if self.ult_cooldown > 0:
            self.ult_cooldown -= game_framework.frame_time
            if self.ult_cooldown < 0:
                self.ult_cooldown = 0

    def handle_event(self, event):
        # 전역 키 눌림 상태 갱신
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.left_pressed = True
            elif event.key == SDLK_d:
                self.right_pressed = True
            elif event.key == SDLK_k:
                if not self.is_slash_unlocked or self.slash_cooldown > 0:
                    return
            elif event.key == SDLK_LSHIFT:
                if self.dash_cooldown > 0:
                    return
            elif event.key == SDLK_l:
                if not self.is_ult_unlocked or self.ult_cooldown > 0:
                    return
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

    def get_bb(self):
        return self.state_machine.get_bb()

    def add_slash_effect(self):
        slash = SlashEffect(self.x, self.y, self.face_dir, self)
        game_world.add_object(slash, 2)
        game_world.add_collision_pair('monster:player_slash', None, slash)

    def handle_collision(self, group, other):
        if group == 'player:monster_attack' and not self.is_hit:
            self.hp -= other.attack_damage
            self.is_hit = True
            print("Player Hit!", self.hp)