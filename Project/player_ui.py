from pico2d import *
from player import Player

class PlayerUI:
    def __init__(self, player):
        self.x, self.y = 50, 650
        self.player = player

    def update(self):
        pass

    def draw(self):
        # Draw health bar
        health_bar_width = 300
        health_bar_height = 20
        health_percentage = self.player.hp / self.player.max_hp
        filled_width = int(health_bar_width * health_percentage)

        border_thickness = 3

        # Draw black border (outer rectangle)
        draw_rectangle(
            self.x - border_thickness,
            self.y - border_thickness,
            self.x + health_bar_width + border_thickness,
            self.y + health_bar_height + border_thickness,
            100, 100, 100, 0, True
        )

        # Draw background of health bar (red)
        draw_rectangle(self.x, self.y, self.x + health_bar_width, self.y + health_bar_height, 255, 0, 0, 0, True)
        # Draw filled part of health bar (green)
        draw_rectangle(self.x, self.y, self.x + filled_width, self.y + health_bar_height, 0, 255, 0, 0, True)


