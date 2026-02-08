import arcade
import math
from constants import BULLET_SPEED


class Bullet(arcade.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__("sprites/bullet.png", 1)
        self.center_x = x
        self.center_y = y

        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        self.change_x = dx / distance * BULLET_SPEED
        self.change_y = dy / distance * BULLET_SPEED

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < -1000 or self.center_x > 1000 or self.center_y < -1000 or self.center_y > 1000:
            self.remove_from_sprite_lists()
