from pico2d import load_image, draw_rectangle
import game_framework
import common
from state_machine import StateMachine
from player import Player
from monster_ui import MonsterUI
from brute_attack import BruteAttack
from damage_text import DamageText
import game_world
import random


# 이벤트 체크 함수
def key_event(e, ev_type, key):
    return e[0] == 'INPUT' and e[1].type == ev_type and e[1].key == key

def attack_player(e) : return e[0] == 'ATTACK_PLAYER'
def attack_finish(e) : return e[0] == 'ATTACK_FINISH'
def find_player(e) : return e[0] == 'FIND_PLAYER'
def lose_player(e) : return e[0] == 'LOSE_PLAYER'
def hit(e) : return e[0] == 'HIT'
def hit_finish(e) : return e[0] == 'HIT_FINISH'
def death(e) : return e[0] == 'DEATH'


PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
BRUTE_SIZE_RATE = (400 / 120)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
#BRUTE 속도 계산
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Death:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,9,69,78),(78,9,66,76),(150,9,65,54),(221,9,60,50),(287,9,87,36),
                       (380,9,86,25),(472,9,88,25),(566,9,88,25),(660,9,88,25),(754,9,88,25),
                       (848,9,88,25),(942,9,88,25),(1036,9,88,25))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'DEATH'
        common.total_monster -= 1

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
        self.action = ((3,98,75,62),(3,98,75,62),(3,98,75,62),(3,98,75,62))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'HIT'

    def exit(self, e):
        pass

    def do(self):
        self.monster.x -= self.monster.face_dir * (RUN_SPEED_PPS / 4) * game_framework.frame_time
        self.monster.anim_progress += 2.0 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        if self.monster.hp <= 0:
            self.monster.state_machine.handle_event(('DEATH', None))

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('HIT_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,169,72,80),(81,169,73,80),(160,169,112,80),(278,169,90,80),(374,169,89,80),
                       (469,169,87,80),(562,169,76,80),(644,169,72,80),(722,169,61,80))
        self.attack = None

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'ATTACK'

    def exit(self, e):
        if self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

    def do(self):
        self.monster.next_frame(self.action)

        if self.monster.frame == 2 and self.attack is None:
            self.attack = BruteAttack(self.monster.x, self.monster.y, self.monster.attack_damage, self.monster)
            game_world.add_object(self.attack, 2)
            game_world.add_collision_pair('player:monster_attack', None, self.attack)

        if self.monster.frame > 2 and self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('ATTACK_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((3,255,73,63),(81,255,78,63),(166,255,73,62),(247,255,68,63))

    def enter(self, e):
        self.monster.frame = random.randint(0, 3)
        self.monster.anim_progress = float(self.monster.frame)
        self.monster.current_state = 'RUN'

    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.5 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        self.monster.move_x()

        if not self.monster.check_near_player():
            # print("Zombie lose Player")
            self.monster.state_machine.handle_event(('LOSE_PLAYER', None))

        if self.monster.check_near_player_attack():
            self.monster.state_machine.handle_event(('ATTACK_PLAYER', None))

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
        self.action = ((3,325,67,62),(76,325,65,62),(147,325,67,62),(220,325,69,60),(295,325,71,60),
                       (372,325,71,60),(449,325,71,60),(526,325,70,61))

    def enter(self, e):
        self.monster.dir = 0
        self.monster.frame = random.randint(0, 7)
        self.monster.anim_progress = float(self.monster.frame)
        self.monster.current_state = 'IDLE'

    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)
        if self.monster.check_near_player():
            # print("Player Near Brute")
            self.monster.state_machine.handle_event(('FIND_PLAYER', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Brute:
    image = None
    def __init__(self):
        self.x, self.y = 940, 165
        self.hp = 300
        self.max_hp = 300

        self.attack_damage = 20

        self.current_state = 'IDLE'

        # 체력 UI
        self.monster_ui_offset_y = 90
        self.monster_ui = MonsterUI(self)
        game_world.add_object(self.monster_ui, 3)

        # 애니메이션 관련 변수
        self.frame = random.randint(0, 7)
        self.anim_progress = float(self.frame)
        if Brute.image is None:
            Brute.image = load_image('Sprite/Brute.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Attack(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: { find_player: self.RUN, hit: self.HIT },
                self.RUN: { lose_player: self.IDLE, hit: self.HIT, attack_player: self.ATTACK },
                self.ATTACK: { attack_finish: self.IDLE, hit: self.HIT },
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

        max_height = 80  # 첫 프레임 높이
        current_height = action[self.frame][3]
        y_offset = self.y - (max_height - current_height) * BRUTE_SIZE_RATE / 2

        # 스크롤링 적용
        screen_x = self.x - common.ground_1.window_left
        screen_y = y_offset - common.ground_1.window_bottom

        if self.face_dir == 1:
            self.image.clip_draw(*rect, screen_x, screen_y,
                                         action[self.frame][2] * BRUTE_SIZE_RATE,
                                         action[self.frame][3] * BRUTE_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', screen_x, screen_y,
                                                   action[self.frame][2] * BRUTE_SIZE_RATE,
                                                   action[self.frame][3] * BRUTE_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * BRUTE_SIZE_RATE / 2
        y_offset = action[self.frame][3] * BRUTE_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 80  # Idle 상태의 기준 높이
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * BRUTE_SIZE_RATE / 2

        if common.is_scrolling:
            screen_x = self.x - common.ground_1.window_left
            screen_y = adjusted_y - common.ground_1.window_bottom
            return (screen_x - x_offset, screen_y - y_offset,
                    screen_x + x_offset, screen_y + y_offset)
        else:
            return (self.x - x_offset, adjusted_y - y_offset,
                    self.x + x_offset, adjusted_y + y_offset)

    def get_bb(self):
        return self.state_machine.get_bb()

    def move_x(self):
        self.x = self.x + self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def check_near_player(self):
        player = game_world.find_object_by_type(Player)
        if player:
            distance = self.x - player.x
            return -500 < distance < 500
        return False

    def check_near_player_attack(self):
        player = game_world.find_object_by_type(Player)
        if player:
            distance = self.x - player.x
            return -200 < distance < 200
        return False

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        if group == 'monster:player_attack' and self.current_state != 'HIT':
            print("Brute Hit by Player Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.base_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.base_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_slash' and self.current_state != 'HIT':
            print("Brute Hit by Player Slash")
            damage_text = DamageText(self.x, self.y + 50, other.player.slash_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.slash_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_ult' and self.current_state != 'HIT':
            print("Brute Hit by Player Ult Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.ult_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.ult_damage
            self.state_machine.handle_event(('HIT', None))