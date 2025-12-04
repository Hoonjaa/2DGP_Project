from pico2d import *
import game_world
from arrow import Arrow
import common

class UltText2:
    font = None
    price_font = None

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.text = '스킬 공격력 + 5'
        self.price = '가격 : 30'
        if UltText2.font == None:
            UltText2.font = load_font('Galmuri14.ttf', 24)
        if UltText2.price_font == None:
            UltText2.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        UltText2.font.draw(self.x, self.y + 50, str(self.text), (0, 0, 0))
        UltText2.price_font.draw(self.x, self.y - 40, str(self.price), (0, 0, 0))

class UltText:
    font = None
    explane_font = None
    price_font = None

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.text = '그림자 스킬 개방'
        self.explane1 = 'L을 눌러 그림자를'
        self.explane2 = '소환하고 주변을'
        self.explane3 = '공격합니다.'
        self.price = '가격 : 200'
        if UltText.font == None:
            UltText.font = load_font('Galmuri14.ttf', 24)
        if UltText.explane_font == None:
            UltText.explane_font = load_font('Galmuri14.ttf', 20)
        if UltText.price_font == None:
            UltText.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        UltText.font.draw(self.x, self.y + 100, str(self.text), (0, 0, 0))
        UltText.explane_font.draw(self.x, self.y + 50, str(self.explane1), (0, 0, 0))
        UltText.explane_font.draw(self.x, self.y + 27, str(self.explane2), (0, 0, 0))
        UltText.explane_font.draw(self.x, self.y + 4, str(self.explane3), (0, 0, 0))
        UltText.price_font.draw(self.x, self.y - 40, str(self.price), (0, 0, 0))

class SlashText2:
    font = None
    price_font = None

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.text = '스킬 공격력 + 10'
        self.price = '가격 : 30'
        if SlashText2.font == None:
            SlashText2.font = load_font('Galmuri14.ttf', 24)
        if SlashText2.price_font == None:
            SlashText2.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        SlashText2.font.draw(self.x, self.y + 50, str(self.text), (0, 0, 0))
        SlashText2.price_font.draw(self.x, self.y - 40, str(self.price), (0, 0, 0))

class SlashText:
    font = None
    explane_font = None
    price_font = None

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.text = '검기 스킬 개방'
        self.explane1 = 'K를 눌러 전방에'
        self.explane2 = '검기를 발사합니다.'
        self.price = '가격 : 100'
        if SlashText.font == None:
            SlashText.font = load_font('Galmuri14.ttf', 24)
        if SlashText.explane_font == None:
            SlashText.explane_font = load_font('Galmuri14.ttf', 20)
        if SlashText.price_font == None:
            SlashText.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        SlashText.font.draw(self.x, self.y + 100, str(self.text), (0, 0, 0))
        SlashText.explane_font.draw(self.x, self.y + 50, str(self.explane1), (0, 0, 0))
        SlashText.explane_font.draw(self.x, self.y + 27, str(self.explane2), (0, 0, 0))
        SlashText.price_font.draw(self.x, self.y - 40, str(self.price), (0, 0, 0))

class HeartText:
    font = None
    price_font = None
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.text = '최대 체력 + 20'
        self.price = '가격 : 10'
        if HeartText.font == None:
            HeartText.font = load_font('Galmuri14.ttf', 24)
        if HeartText.price_font == None:
            HeartText.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        HeartText.font.draw(self.x, self.y, str(self.text), (0, 0, 0))
        HeartText.price_font.draw(self.x, self.y - 30, str(self.price), (0, 0, 0))

class AttackText:
    font = None
    price_font = None
    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.text = '기본 공격력 + 5'
        self.price = '가격 : 10'
        if AttackText.font == None:
            AttackText.font = load_font('Galmuri14.ttf', 24)
        if AttackText.price_font == None:
            AttackText.price_font = load_font('Galmuri14.ttf', 15)

    def update(self):
        pass

    def draw(self):
        AttackText.font.draw(self.x, self.y, str(self.text), (0, 0, 0))
        AttackText.price_font.draw(self.x, self.y - 30, str(self.price), (0, 0, 0))

class ForgePannel:
    def __init__(self):
        self.image = load_image('Sprite/forge_ui.png')
        self.arrow_positions = ((285, 590), (718, 590), (285, 375), (718, 375)) # 임시값
        self.arrow = Arrow(*self.arrow_positions[0])
        self.current_selection = 0
        game_world.add_object(self.arrow,4)

        self.attack_text = AttackText(400, 500)
        self.heart_text = HeartText(833, 500)
        self.slash_text = SlashText(400, 200)
        self.slash_text2 = SlashText2(400, 200)
        self.ult_text = UltText(833, 200)
        self.ult_text2 = UltText2(833, 200)

    def draw(self):
        self.image.draw(640, 360)
        self.attack_text.draw()
        self.heart_text.draw()
        if common.player.is_slash_unlocked == False: self.slash_text.draw()
        else: self.slash_text2.draw()
        if common.player.is_ult_unlocked == False: self.ult_text.draw()
        else: self.ult_text2.draw()

    def update(self):
        self.arrow.change_position(*self.arrow_positions[self.current_selection])

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.current_selection = (self.current_selection + 1) % len(self.arrow_positions)
            elif event.key == SDLK_s:
                self.current_selection = (self.current_selection + 2) % len(self.arrow_positions)
            elif event.key == SDLK_a:
                self.current_selection = (self.current_selection - 1) % len(self.arrow_positions)
            elif event.key == SDLK_w:
                self.current_selection = (self.current_selection - 2) % len(self.arrow_positions)
            elif event.key == SDLK_p:
                common.player.jewel += 500  # 디버그용 보석 추가
            elif event.key == SDLK_SPACE:
                if self.current_selection == 0:
                    if common.player.jewel >= 10:
                        common.player.base_damage += 5
                        common.player.jewel -= 10
                elif self.current_selection == 1:
                    if common.player.jewel >= 10:
                        common.player.max_hp += 20
                        common.player.hp += 20
                        common.player.jewel -= 10
                elif self.current_selection == 2:
                    if common.player.is_slash_unlocked == False:
                        if common.player.jewel >= 100:
                            common.player.is_slash_unlocked = True
                            common.player.jewel -= 100
                    else:
                        if common.player.jewel >= 30:
                            common.player.slash_damage += 10
                            common.player.jewel -= 30
                elif self.current_selection == 3:
                    if common.player.is_ult_unlocked == False:
                        if common.player.jewel >= 200:
                            common.player.is_ult_unlocked = True
                            common.player.jewel -= 200
                    else:
                        if common.player.jewel >= 30:
                            common.player.ult_damage += 5
                            common.player.jewel -= 30