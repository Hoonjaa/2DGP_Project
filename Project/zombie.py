from pico2d import load_image, draw_rectangle
import game_world
import game_framework
from player import Player
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


PIXEL_PER_METER = (1.0 / 0.02) # 1 pixel 2 cm
# 중력 처리
GRAVITY_MPS2 = 9.8
GRAVITY_PPS2 = GRAVITY_MPS2 * PIXEL_PER_METER
# 애니메이션 속도 계산
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 좀비 크기 비율
ZOMBIE_SIZE_RATE = (200 / 120)
# 좀비 속도 계산
RUN_SPEED_KMPH = 15.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Death:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,9,38,54),(48,9,37,56),(91,9,45,57),(142,9,44,56),(192,9,41,50),
                       (239,9,44,42),(289,9,39,42),(334,9,34,42),(374,9,42,42),(422,9,60,25),
                       (488,9,63,12),(557,9,64,13),(630,9,64,11))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'DEATH'

    def exit(self, e):
        pass

    def do(self):
        self.monster.anim_progress += 1 * game_framework.frame_time * len(self.action)
        self.monster.frame = int(self.monster.anim_progress) % len(self.action)

        if self.monster.frame == len(self.action) - 1:
            game_world.remove_object(self.monster)

    def draw(self):
        frame = self.monster.frame
        size_x, size_y = self.action[self.monster.frame][2] * ZOMBIE_SIZE_RATE, self.action[self.monster.frame][3] * ZOMBIE_SIZE_RATE
        x_render = self.monster.x + (self.action[self.monster.frame][2] - 48) / 2 * ZOMBIE_SIZE_RATE * self.monster.face_dir
        y_render = self.monster.y + (self.action[self.monster.frame][3] - 48) / 2 * ZOMBIE_SIZE_RATE

        rect = self.action[frame]
        if self.monster.face_dir == 1:
            self.monster.image.clip_draw(*rect, x_render, y_render, size_x, size_y)
        else:
            self.monster.image.clip_composite_draw(*rect, 0, 'h', x_render, y_render, size_x, size_y)

    def get_bb(self):
        pass

class Hit:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,73,54,66),(4,73,54,66),(4,73,54,66),(4,73,54,66))

    def enter(self, e):
        self.monster.frame = 0
        self.monster.anim_progress = 0.0
        self.monster.current_state = 'HIT'

    def exit(self, e):
        pass

    def do(self):
        self.monster.x -= self.monster.face_dir * (RUN_SPEED_PPS / 4) * game_framework.frame_time
        self.monster.next_frame(self.action)

        if self.monster.hp <= 0:
            self.monster.state_machine.handle_event(('DEATH', None))

        if self.monster.frame == len(self.action) - 1:
            self.monster.state_machine.handle_event(('HIT_FINISH', None))

    def draw(self):
        self.monster.draw_current(self.action)
        draw_rectangle(*self.get_bb(), 255, 0, 0)

    def get_bb(self):
        x_offset = self.action[self.monster.frame][2] * ZOMBIE_SIZE_RATE / 2
        y_offset = self.action[self.monster.frame][3] * ZOMBIE_SIZE_RATE / 2
        return (self.monster.x - x_offset, self.monster.y - y_offset, self.monster.x + x_offset, self.monster.y + y_offset)


class Run:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((164,280,47,62),(217,280,52,61),(275,280,52,58),(344,280,52,58),(416,280,53,58),(475,280,53,59))

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
        x_offset = self.action[self.monster.frame][2] * ZOMBIE_SIZE_RATE / 2
        y_offset = self.action[self.monster.frame][3] * ZOMBIE_SIZE_RATE / 2
        return (self.monster.x - x_offset, self.monster.y - y_offset, self.monster.x + x_offset, self.monster.y + y_offset)


class Idle:
    def __init__(self, monster):
        self.monster = monster
        self.action = ((4,420,43,61),(53,420,44,60),(103,420,45,59),(154,420,46,59),(206,420,45,60),(257,420,44,61))

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
        x_offset = self.action[self.monster.frame][2] * ZOMBIE_SIZE_RATE / 2
        y_offset = self.action[self.monster.frame][3] * ZOMBIE_SIZE_RATE / 2
        return (self.monster.x - x_offset, self.monster.y - y_offset, self.monster.x + x_offset, self.monster.y + y_offset)


class Zombie:
    image = None
    def __init__(self):
        self.x, self.y = 740, 90
        self.hp = 200

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Zombie.image is None:
            Zombie.image = load_image('Sprite/Zombie.png')

        # 낙하 관련 변수
        self.ground_y = self.y
        self.dropSpeed = 8.0 * PIXEL_PER_METER

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
                self.IDLE: { find_player: self.RUN, hit: self.HIT },
                self.RUN: { lose_player: self.IDLE, hit: self.HIT },
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
        if self.face_dir == 1:
            self.image.clip_draw(*rect, self.x, self.y, action[self.frame][2] * ZOMBIE_SIZE_RATE, action[self.frame][3] * ZOMBIE_SIZE_RATE)
        else:
            self.image.clip_composite_draw(*rect, 0, 'h', self.x, self.y, action[self.frame][2] * ZOMBIE_SIZE_RATE, action[self.frame][3] * ZOMBIE_SIZE_RATE)

    def move_x(self):
        self.x = self.x + self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 들어온 외부 키 입력을 상태머신에게 전달하기 위해 튜플화 시킨후 전달
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.state_machine.get_bb()

    def check_near_player(self):
        player = game_world.find_object_by_type(Player)
        if player:
            distance = self.x - player.x
            return -300 < distance < 300
        return False

    def handle_collision(self, group, other):
        if group == 'zombie:player_attack' and self.current_state != 'HIT':
            print("Zombie Hit by Player Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.base_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.base_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'zombie:player_slash' and self.current_state != 'HIT':
            print("Zombie Hit by Player Slash")
            damage_text = DamageText(self.x, self.y + 50, other.player.slash_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.slash_damage
            self.state_machine.handle_event(('HIT', None))

        if group == 'zombie:player_ult' and self.current_state != 'HIT':
            print("Zombie Hit by Player Ult Attack")
            damage_text = DamageText(self.x, self.y + 50, other.player.ult_damage)
            game_world.add_object(damage_text, 2)
            self.hp -= other.player.ult_damage
            self.state_machine.handle_event(('HIT', None))