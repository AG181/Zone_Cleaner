import arcade
from views.game_view import GameView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ZONE CLEANER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("PRESS ENTER TO START", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(GameView())
