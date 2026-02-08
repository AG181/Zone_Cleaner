import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os
from views.menu_view import MenuView


class GameOverView(arcade.View):
    def __init__(self, score, win):
        super().__init__()
        self.score = score
        self.win = win

        base_path = os.path.dirname(os.path.abspath(__file__))
        score_file = os.path.join(base_path, "..", "data", "scores.txt")
        os.makedirs(os.path.dirname(score_file), exist_ok=True)
        if not os.path.exists(score_file):
            with open(score_file, "w") as f:
                f.write("0")

        with open(score_file, "r") as f:
            best = int(f.read())

        if self.score > best:
            with open(score_file, "w") as f:
                f.write(str(self.score))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        text = "ПОБЕДА" if self.win else "ПОРАЖЕНИЕ"
        arcade.draw_text(text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60,
                         arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text(f"Счёт: {self.score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 24, anchor_x="center")
        arcade.draw_text("ENTER — В МЕНЮ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                         arcade.color.GRAY, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(MenuView())
