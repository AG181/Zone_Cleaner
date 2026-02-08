import arcade
import math


class Enemy(arcade.Sprite):
    def __init__(self, x, y, speed=2):
        super().__init__("sprites/enemy.png", 1)
        self.center_x = x
        self.center_y = y
        self.speed = speed

    def follow_player(self, player):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.change_x = dx / distance * self.speed
            self.change_y = dy / distance * self.speed
        else:
            self.change_x = 0
            self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
