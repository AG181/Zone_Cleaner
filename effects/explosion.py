import arcade
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.change_x = random.uniform(-2, 2)
        self.change_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)

    def update(self):
        self.x += self.change_x
        self.y += self.change_y
        self.life -= 1


class Explosion:
    def __init__(self, x, y, count=15):
        self.particles = [Particle(x, y) for _ in range(count)]

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self):
        for p in self.particles:
            arcade.draw_circle_filled(p.x, p.y, 3, arcade.color.ORANGE)
