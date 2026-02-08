import arcade
from constants import PLAYER_SPEED


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("sprites/player.png", 1)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
