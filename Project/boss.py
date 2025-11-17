from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import random
from player import Player
from boss_attack import BossAttack
from boss_charge_attack import BossChargeAttack
from state_machine import StateMachine


# 이벤트 체크 함수
def key_event(e, ev_type, key):
    return e[0] == 'INPUT' and e[1].type == ev_type and e[1].key == key

def charge_attack_player(e) : return e[0] == 'CHARGE_ATTACK_PLAYER'
def charge_attack_finish(e) : return e[0] == 'CHARGE_ATTACK_FINISH'
def attack_player(e) : return e[0] == 'ATTACK_PLAYER'
def attack_finish(e) : return e[0] == 'ATTACK_FINISH'
def find_player(e) : return e[0] == 'FIND_PLAYER'
def lose_player(e) : return e[0] == 'LOSE_PLAYER'
def hit(e) : return e[0] == 'HIT'
def hit_finish(e) : return e[0] == 'HIT_FINISH'
def death(e) : return e[0] == 'DEATH'


PIXEL_PER_METER = (1.0 / 0.02)
# BRUTE 크기 비율
BOSS_SIZE_RATE = (300 / 160)
# 애니메이션 속도
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
#BRUTE 속도 계산
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Death:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((415,271,89,91),(513,271,83,93),(605,271,86,92),(700,271,89,91),(798,271,83,93),(890,271,86,92))

    def enter(self, e):
        self.monster.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 0.7 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Skill:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,683,66,107),(82,718,99,72),(190,723,100,67),(299,656,163,134),(471,652,168,138),
                       (648,693,174,97),(831,673,175,117),(1015,682, 177,108),(1201,675,182,115),(1392,724,75,66),
                       (1476,724,75,66),(1560,724,75,66))

    def enter(self, e):
        self.monster.dir = 0
        self.monster.y += 10

    def exit(self, e):
        self.monster.y -= 10

    def do(self):
        self.monster.anim_progress += 0.8 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Charge_Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1060,129,101),(145,1061,126,98),(280,1061,126,100),(7,1060,129,101),(145,1061,126,98),
                       (280,1061,126,100),(415,1027,163,134),(587,1023,168,138),(764,1064,174,97),(947,1044,175,117),
                       (1131,1053,177,108),(1317,1046,182,115))
        self.attack = None

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'CHARGE_ATTACK'
        self.monster.y += 10

    def exit(self, e):
        self.monster.y -= 10
        if self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

    def do(self):
        self.monster.next_frame(self.action)

        if self.monster.frame == 6 and self.attack is None:
            self.attack = BossChargeAttack(self.monster.x, self.monster.y, self.monster.attack_damage, self.monster.face_dir, self.monster)
            game_world.add_object(self.attack, 2)
            game_world.add_collision_pair('player:monster_attack', None, self.attack)

        if self.monster.frame > 8 and self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('CHARGE_ATTACK_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return (self.monster.x - 60 * BOSS_SIZE_RATE, self.monster.y - 30 * BOSS_SIZE_RATE,
                self.monster.x + 23 * BOSS_SIZE_RATE, self.monster.y + 60 * BOSS_SIZE_RATE)


class Attack:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1345,66,107),(82,1380,99,72),(190,1382,100,70),(299,1319,180,133),(488,1314,180,138),
                       (677,1319,168,133),(854,1335,171,117),(1034,1343,174,109),(1217,1338,175,114))
        self.attack = None

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'ATTACK'
        self.monster.y += 10

    def exit(self, e):
        self.monster.y -= 10
        if self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

    def do(self):
        self.monster.next_frame(self.action)

        if self.monster.frame == 3 and self.attack is None:
            self.attack = BossAttack(self.monster.x, self.monster.y, self.monster.attack_damage, self.monster.face_dir, self.monster)
            game_world.add_object(self.attack, 2)
            game_world.add_collision_pair('player:monster_attack', None, self.attack)

        if self.monster.frame > 5 and self.attack:
            game_world.remove_object(self.attack)
            self.attack = None

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('ATTACK_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return (self.monster.x - 50 * BOSS_SIZE_RATE, self.monster.y - 20 * BOSS_SIZE_RATE,
                self.monster.x + 28 * BOSS_SIZE_RATE, self.monster.y + 60 * BOSS_SIZE_RATE)


class Dash:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1782,95,68),(111,1782,95,68),(215,1782,99,68),(323,1782,101,68),(433,1782,103,68),(545,1782,94,68))

    def enter(self, e):
        self.monster.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.monster.next_frame(self.action)

    def draw(self):
        self.monster.draw_current(self.action)

    def get_bb(self):
        pass


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1867,84,75),(100,1867,84,75),(193,1867,76,77),(278,1867,84,75),(371,1867,84,75),(464,1867,76,77))

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
            self.monster.state_machine.handle_event(('LOSE_PLAYER', None))

        if self.monster.check_near_player_attack():
            # ATTACK과 CHARGE_ATTACK 중 랜덤 선택
            attack_type = random.choice(['ATTACK_PLAYER', 'CHARGE_ATTACK_PLAYER'])
            self.monster.state_machine.handle_event((attack_type, None))

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
        return (self.monster.x - 30 * BOSS_SIZE_RATE, self.monster.y - 20 * BOSS_SIZE_RATE,
                self.monster.x + 35 * BOSS_SIZE_RATE, self.monster.y + 35 * BOSS_SIZE_RATE)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((7,1959,70,79),(86,1959,73,79),(168,1959,75,79),(252,1959,77,79),(338,1959,79,79),(426,1959,74,79))

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
            # print("Player Near Brute")
            self.monster.state_machine.handle_event(('FIND_PLAYER', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        return (self.monster.x - 35 * BOSS_SIZE_RATE, self.monster.y - 20 * BOSS_SIZE_RATE,
                self.monster.x + 18 * BOSS_SIZE_RATE, self.monster.y + 40 * BOSS_SIZE_RATE)


class Boss:
    image = None

    def __init__(self):
        self.x, self.y = 300, 80
        self.hp = 500

        self.attack_damage = 20
        self.charge_attack_damage = 40
        self.skill_damage = 30

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Boss.image is None:
            Boss.image = load_image('Sprite/Reaper.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0

        # 상태 머신 초기화
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.DASH = Dash(self)
        self.ATTACK = Attack(self)
        self.CHARGE_ATTACK = Charge_Attack(self)
        self.SKILL = Skill(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: { find_player: self.RUN },
                self.RUN: { lose_player: self.IDLE, attack_player: self.ATTACK, charge_attack_player: self.CHARGE_ATTACK },
                self.DASH: {},
                self.ATTACK: { attack_finish: self.IDLE },
                self.CHARGE_ATTACK: { charge_attack_finish: self.IDLE },
                self.SKILL: {},
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
        y_offset = self.y - (max_height - current_height) * BOSS_SIZE_RATE / 2
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, y_offset,
                                 action[self.frame][2] * BOSS_SIZE_RATE,
                                 action[self.frame][3] * BOSS_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, y_offset,
                                           action[self.frame][2] * BOSS_SIZE_RATE,
                                           action[self.frame][3] * BOSS_SIZE_RATE)

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
            return -150 < distance < 150
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