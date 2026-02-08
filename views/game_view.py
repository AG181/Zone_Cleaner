import arcade
import random
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_HEALTH
from sprites.player import Player
from sprites.bullet import Bullet
from sprites.enemy import Enemy
from effects.explosion import Explosion
from arcade.camera import Camera2D


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.bullet_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()

        self.explosion_list = []

        self.camera = Camera2D()

        self.score = 0
        self.player_health = PLAYER_HEALTH
        self.level = 1
        self.max_levels = 3

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.shoot_sound = arcade.load_sound(os.path.join(base_path, "..", "sounds", "shot.wav"))
        self.hit_sound = arcade.load_sound(os.path.join(base_path, "..", "sounds", "hit.wav"))
        music_path = os.path.join(base_path, "..", "sounds", "music.wav")
        if os.path.exists(music_path):
            self.music = arcade.load_sound(music_path)
            arcade.play_sound(self.music)
        else:
            self.music = None

        self.load_level()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        for exp in self.explosion_list:
            exp.draw()

        arcade.draw_text(f"HP: {self.player_health}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16)
        arcade.draw_text(f"Level: {self.level}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        self.player_list.update(delta_time)
        self.bullet_list.update(delta_time)
        self.enemy_list.update(delta_time)

        for enemy in self.enemy_list:
            enemy.follow_player(self.player)

        for exp in self.explosion_list:
            exp.update()
        self.explosion_list = [e for e in self.explosion_list if len(e.particles) > 0]

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    self.enemy_list.remove(enemy)
                    self.score += 10
                    self.explosion_list.append(Explosion(enemy.center_x, enemy.center_y))
                    arcade.play_sound(self.hit_sound)

        hit_enemies = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hit_enemies:
            self.enemy_list.remove(enemy)
            self.player_health -= 10
            self.explosion_list.append(Explosion(enemy.center_x, enemy.center_y))

        if self.player_health <= 0:
            from views.game_over_view import GameOverView
            self.window.show_view(GameOverView(self.score, False))

        if len(self.enemy_list) == 0:
            self.level += 1
            if self.level > self.max_levels:
                from views.game_over_view import GameOverView
                self.window.show_view(GameOverView(self.score, True))
            else:
                self.load_level()

        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = PLAYER_SPEED
        if key == arcade.key.S:
            self.player.change_y = -PLAYER_SPEED
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            world_x = x + self.camera.position[0]
            world_y = y + self.camera.position[1]

            bullet = Bullet(self.player.center_x, self.player.center_y, world_x, world_y)
            self.bullet_list.append(bullet)
            arcade.play_sound(self.shoot_sound)

    def center_camera_to_player(self):
        target_x = self.player.center_x - SCREEN_WIDTH / 2
        target_y = self.player.center_y - SCREEN_HEIGHT / 2

        current_x, current_y = self.camera.position
        lerp = 0.1
        new_x = current_x + (target_x - current_x) * lerp
        new_y = current_y + (target_y - current_y) * lerp

        self.camera.position = (new_x, new_y)

    def load_level(self):
        self.enemy_list.clear()
        count = self.level * 8
        for _ in range(count):
            x = random.randint(-800, 800)
            y = random.randint(-800, 800)
            self.enemy_list.append(Enemy(x, y, speed=2))
