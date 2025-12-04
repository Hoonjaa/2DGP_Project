from pico2d import *
import game_world
from arrow import Arrow

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

    def draw(self):
        self.image.draw(640, 360)
        self.attack_text.draw()

    def update(self):
        self.arrow.change_position(*self.arrow_positions[self.current_selection])

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.current_selection = (self.current_selection + 1) % len(self.arrow_positions)
            elif event.key == SDLK_DOWN:
                self.current_selection = (self.current_selection + 2) % len(self.arrow_positions)
            elif event.key == SDLK_LEFT:
                self.current_selection = (self.current_selection - 1) % len(self.arrow_positions)
            elif event.key == SDLK_UP:
                self.current_selection = (self.current_selection - 2) % len(self.arrow_positions)