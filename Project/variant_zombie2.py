from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import common
from player import Player
from monster_ui import MonsterUI
from damage_text import DamageText
from state_machine import StateMachine


# 이벤트 체크 함수
def key_event(e, ev_type, key):
    return e[0] == 'INPUT' and e[1].type == ev_type and e[1].key == key

def find_player(e) : return e[0] == 'FIND_PLAYER'
def lose_player(e) : return e[0] == 'LOSE_PLAYER'
def hit(e) : return e[0] == 'HIT'
def hit_finish(e) : return e[0] == 'HIT_FINISH'
def death(e) : return e[0] == 'DEATH'


PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
VZ2_SIZE_RATE = (300 / 120)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 속도 계산
RUN_SPEED_KMPH = 18.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Death:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,98,50,55),(60,98,56,44),(122,98,60,27),(188,98,46,32),(240,98,62,33),
                       (312,98,76,12),(395,98,78,12))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'DEATH'


    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)
        if self.monster.frame == len(self.action) - 1:
            game_world.remove_object(self.monster.monster_ui)
            game_world.remove_object(self.monster)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Hit:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,161,33,55),(4,161,33,55),(4,161,33,55),(4,161,33,55))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'HIT'


    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 2.0 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        self.monster.x -= self.monster.face_dir * (RUN_SPEED_PPS / 4) * game_framework.frame_time

        if self.monster.hp <= 0:
            self.monster.state_machine.handle_event(('DEATH', None))

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('HIT_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,289,26,58),(36,289,27,57),(69,289,20,58),(95,289,18,59),(119,289,23,58),
                       (148,289,26,57),(180,289,26,58),(212,289,26,59))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'RUN'


    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)
        self.monster.move_x()

        if not self.monster.check_near_player():
            # print("Zombie lose Player")
            self.monster.state_machine.handle_event(('LOSE_PLAYER', None))

        player = game_world.find_object_by_type(Player)
        if player and self.monster.x > player.x + 20:
            self.monster.dir = -1
            self.monster.face_dir = -1
        elif player and self.monster.x < player.x - 20:
            self.monster.dir = 1
            self.monster.face_dir = 1
        else:
            self.monster.dir = 0

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,356,29,58),(39,356,29,57),(74,356,29,57),(109,356,28,57),(143,356,28,57),
                       (177,356,28,58),(211,356,28,58),(245,356,29,58))

    def enter(self, e):
        self.monster.dir = 0
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'IDLE'

    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)
        if self.monster.check_near_player():
            # print("Player Near Zombie")
            self.monster.state_machine.handle_event(('FIND_PLAYER', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class VZ2:
    image = None
    def __init__(self):
        self.x, self.y = 600, 115
        self.hp = 200
        self.max_hp = 200

        self.attack_damage = 15

        self.current_state = 'IDLE'

        # 체력 UI
        self.monster_ui_offset_y = 80
        self.monster_ui = MonsterUI(self)
        game_world.add_object(self.monster_ui, 3)

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if VZ2.image is None:
            VZ2.image = load_image('Sprite/Variant Zombie2.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {find_player: self.RUN, hit: self.HIT},
                self.RUN: {lose_player: self.IDLE, hit: self.HIT},
                self.HIT: {hit_finish: self.IDLE, death: self.DEATH},
                self.DEATH: {},
            }
        )

    def next_frame(self, action):
        # 진행 누적
        self.anim_progress += ACTION_PER_TIME * game_framework.frame_time * len(action)
        # 정수 프레임 산출
        self.frame = int(self.anim_progress) % len(action)

    def draw_current(self, action):
        idx = self.frame % len(action)
        rect = action[idx]

        max_height = 60  # 첫 프레임 높이
        current_height = action[self.frame][3]
        y_offset = self.y - (max_height - current_height) * VZ2_SIZE_RATE / 2

        # 스크롤링 적용
        screen_x = self.x - common.ground_1.window_left
        screen_y = y_offset - common.ground_1.window_bottom

        if self.face_dir == 1:
            self.image.clip_draw(*rect, screen_x, screen_y,
                                 action[self.frame][2] * VZ2_SIZE_RATE,
                                 action[self.frame][3] * VZ2_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', screen_x, screen_y,
                                           action[self.frame][2] * VZ2_SIZE_RATE,
                                           action[self.frame][3] * VZ2_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * VZ2_SIZE_RATE / 2
        y_offset = action[self.frame][3] * VZ2_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 58
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * VZ2_SIZE_RATE / 2

        if common.is_scrolling:
            screen_x = self.x - common.ground_1.window_left
            screen_y = adjusted_y - common.ground_1.window_bottom
            return (screen_x - x_offset, screen_y - y_offset,
                    screen_x + x_offset, screen_y + y_offset)
        else:
            return (self.x - x_offset, adjusted_y - y_offset,
                    self.x + x_offset, adjusted_y + y_offset)

    def move_x(self):
        self.x = self.x + self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def check_near_player(self):
        player = game_world.find_object_by_type(Player)
        if player:
            distance = self.x - player.x
            return -300 < distance < 300
        return False

    def get_bb(self):
        return self.state_machine.get_bb()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        if group == 'monster:player_attack' and self.current_state != 'HIT':
            print("Variant_Zombie2 Hit by Player Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.base_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.base_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_slash' and self.current_state != 'HIT':
            print("Variant_Zombie2 Hit by Player Slash")
            damage_text = DamageText(self.x, self.y + 50, other.player.slash_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.slash_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_ult' and self.current_state != 'HIT':
            print("Variant_Zombie2 Hit by Player Ult Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.ult_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.ult_damage
            self.state_machine.handle_event(('HIT', None))