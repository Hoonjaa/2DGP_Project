from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import common
from player import Player
from monster_ui import MonsterUI
from damage_text import DamageText
from vz2_attack import VZ2Attack
from state_machine import StateMachine


# 이벤트 체크 함수
def key_event(e, ev_type, key):
    return e[0] == 'INPUT' and e[1].type == ev_type and e[1].key == key

def attack_player(e) : return e[0] == 'ATTACK_PLAYER'
def attack_finish(e) : return e[0] == 'ATTACK_FINISH'
def find_player(e) : return e[0] == 'FIND_PLAYER'
def lose_player(e) : return e[0] == 'LOSE_PLAYER'
def teleport_in_finish(e) : return e[0] == 'TP_IN_FINISH'
def teleport_out_finish(e) : return e[0] == 'TP_OUT_FINISH'
def hit(e) : return e[0] == 'HIT'
def hit_finish(e) : return e[0] == 'HIT_FINISH'
def death(e) : return e[0] == 'DEATH'


PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
VZ1_SIZE_RATE = (250 / 120)
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
        self.action = ((2,10,45,62),(52,10,62,59),(119,10,74,35),(198,10,61,51),(264,10,69,44),
                       (338,10,75,42),(418,10,79,30),(502,10,80,29),(587,10,69,44),(661,10,72,42),
                       (738,10,74,20),(817,10,74,21))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'DEATH'
        common.total_monster -= 1


    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 0.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

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
        self.action = ((2,237,45,67),(2,237,45,67),(2,237,45,67),(2,237,45,67))

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


class Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,541,61,66),(68,541,57,68),(130,541,59,65),(194,541,92,59),(291,541,60,45),
                       (356,541,60,43),(421,541,59,43),(485,541,60,47),(550,541,53,53),(608,541,40,58))
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
            self.attack = VZ2Attack(self.monster.x, self.monster.y, self.monster.attack_damage, self.monster.face_dir, self.monster)
            game_world.add_object(self.attack, 2)
            game_world.add_collision_pair('player:monster_attack', None, self.attack)

        if self.monster.frame > 3 and self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('ATTACK_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Teleport_Out:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,756,52,64),(59,756,56,63),(120,756,56,57),(181,756,49,60))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'TP_OUT'

        player = game_world.find_object_by_type(Player)
        self.monster.x = player.x + (100 * -player.face_dir)
        if self.monster.x <= player.x:
            self.monster.face_dir = 1
        else:
            self.monster.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('ATTACK_PLAYER', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Teleport_In:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,676,40,65),(47,676,44,67),(96,676,45,72),(146,676,45,68))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'TP_IN'

    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('TP_IN_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return self.monster.bb_operation(self.action)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((2,915,45,61),(52,915,47,59),(104,915,49,57),(158,915,52,55),(215,915,53,54),
                       (273,915,54,54),(332,915,54,56),(391,915,52,58),(448,915,51,59),(504,915,48,60))

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


class VZ1:
    image = None
    def __init__(self):
        self.x, self.y = 700, 105
        self.hp = 150
        self.max_hp = 150

        self.attack_damage = 20

        self.current_state = 'IDLE'

        # 체력 UI
        self.monster_ui_offset_y = 90
        self.monster_ui = MonsterUI(self)
        game_world.add_object(self.monster_ui, 3)

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if VZ1.image is None:
            VZ1.image = load_image('Sprite/Variant Zombie1.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.TP_IN = Teleport_In(self)
        self.TP_OUT = Teleport_Out(self)
        self.ATTACK = Attack(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: { find_player: self.TP_IN, hit: self.HIT },
                self.TP_IN: { teleport_in_finish: self.TP_OUT, hit: self.HIT },
                self.TP_OUT: { attack_player: self.ATTACK, hit: self.HIT },
                self.ATTACK: { attack_finish: self.IDLE, hit: self.HIT },
                self.HIT: { hit_finish: self.IDLE, death: self.DEATH },
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
        y_offset = self.y - (max_height - current_height) * VZ1_SIZE_RATE / 2

        # 스크롤링 적용
        screen_x = self.x - common.ground_1.window_left
        screen_y = y_offset - common.ground_1.window_bottom

        if self.face_dir == 1:
            self.image.clip_draw(*rect, screen_x, screen_y,
                                 action[self.frame][2] * VZ1_SIZE_RATE,
                                 action[self.frame][3] * VZ1_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', screen_x, screen_y,
                                           action[self.frame][2] * VZ1_SIZE_RATE,
                                           action[self.frame][3] * VZ1_SIZE_RATE)

    def bb_operation(self, action):
        x_offset = action[self.frame][2] * VZ1_SIZE_RATE / 2
        y_offset = action[self.frame][3] * VZ1_SIZE_RATE / 2
        # draw_current와 동일한 y 위치 조정
        max_height = 61
        current_height = action[self.frame][3]
        adjusted_y = self.y - (max_height - current_height) * VZ1_SIZE_RATE / 2

        if common.is_scrolling:
            screen_x = self.x - common.ground_1.window_left
            screen_y = adjusted_y - common.ground_1.window_bottom
            return (screen_x - x_offset, screen_y - y_offset,
                    screen_x + x_offset, screen_y + y_offset)
        else:
            return (self.x - x_offset, adjusted_y - y_offset,
                    self.x + x_offset, adjusted_y + y_offset)

    def check_near_player(self):
        player = game_world.find_object_by_type(Player)
        if player:
            distance = self.x - player.x
            return -400 < distance < 400
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
            print("Variant_Zombie1 Hit by Player Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.base_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.base_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_slash' and self.current_state != 'HIT':
            print("Variant_Zombie1 Hit by Player Slash")
            damage_text = DamageText(self.x, self.y + 50, other.player.slash_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.slash_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'monster:player_ult' and self.current_state != 'HIT':
            print("Variant_Zombie1 Hit by Player Ult Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.ult_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.ult_damage
            self.state_machine.handle_event(('HIT', None))